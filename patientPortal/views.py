from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.db import models
from .accessoryScripts.checkGroup import is_patient, is_therapist
from .DB_Extractor import get_personal_info ,get_patient_info
from. forms import MyPersonalInformationForm
from. forms import MyContactInformationForm
import json
from .models import notification, Todo
from .accessoryScripts.resourceManager import fixDict, removeDictKey
import datetime


# PATIENT VIEWS #
def patientDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        return render(
            request, 'patientPortal/patientDashboard.html', context={'first_name': first_name, 'last_name': last_name},
        )
    else:
        return redirect('/portal/therapist')


def MyPersonalInformation(request):

    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        from patientPortal.apiScripts.exports import get_specific_data_by_id
        from patientPortal.apiScripts.helper import create_redcap_event_name
        from .modelHandlers.users import get_newest_cohort_data
        from .models import CohortData, UserProfile

        userProfile = UserProfile.objects.get(user=request.user) #fetches the user UserProfile for user
        therapist = (userProfile.therapist_user)                 #gets the therapist user from user

        cohort_data = get_newest_cohort_data(request.user)           #Returns all the cohort data for user
        patient_id = cohort_data['record_id']                     #Gets the values from the newest input
        cohort_num = cohort_data['cohort_num']

        #This can remain hardcoded as only the admin portion contains patient demographics
        event_prefix = 'admin'
        redcap_event = create_redcap_event_name(event_prefix,cohort_num)

        #fields patient will be able to edit
        fields_of_interest = ['name','contactphone','adline1','adline2','dob','email','emergencycontact','emergencycontactnum']
        patient_data = get_specific_data_by_id(redcap_event,patient_id,fields_of_interest)

        if request.method == 'POST':
            from .accessoryScripts.CompareForms import compare_info
            from .modelHandlers.notifications import create_info_notification
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            request_dict = fixDict(request_dict);
            request_dict = removeDictKey(request_dict, 'csrfmiddlewaretoken')
            request_dict = removeDictKey(request_dict, 'form_type')  #TODO remove this from the front end request

            changes = compare_info(patient_data, request_dict) # we dont need fields_of_interest as a param here
            create_info_notification(therapist, request.user, changes)
            print(request.user.first_name)
            return HttpResponse(json.dumps({'patient_name':request.user.first_name}))

        # This is on the get request
        return render(request, 'patientPortal/information.html', context = patient_data)

    else:
        return redirect('/portal/therapist')


def myprogress(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        if request.method == "GET":
            request_query_dict = request.GET;
            request_dict = dict(request_query_dict);
            if not bool(request_dict): # empty get request
                return render_to_response('patientPortal/myprogress.html')
            # If get request is not empty this will execute
            from patientPortal.modelHandlers.appointments import get_appointments
            import calendar
            appts = get_appointments(request.user,'patient')
            months = {}
            appts_attended = 0;
            total_appts = 0;
            for appt in appts:
                month = int(appt['date'].split('-')[1])
                month = calendar.month_name[month]
                if appt['attended']:
                    appts_attended += 1;
                    if month not in months:
                        months[month] = 1
                    else:
                        months[month] += 1
                total_appts += 1;
            appts_left = total_appts - appts_attended
            return HttpResponse(json.dumps({'months':months,'appts_left':appts_left,'appts_attended':appts_attended}))



    else:
        return redirect('/portal/therapist')


def exercise(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        return render_to_response('patientPortal/exercise.html')
    else:
        return redirect('/portal/therapist')

@csrf_exempt
def patientCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        import json
        if request.method == "GET":
            request_query_dict = request.GET;
            request_dict = dict(request_query_dict);
            if not bool(request_dict):  # Empty get request
                return render_to_response('patientPortal/patientCalendar.html')
            else:
                from patientPortal.modelHandlers.appointments import get_appointments
                appointments = get_appointments(request.user,'patient')
                return HttpResponse(json.dumps({'appts':appointments}))

        #Only post requests will make it here
        request_query_dict = request.POST;
        request_delete = dict(request_query_dict);

        if bool(request_delete):
            date = request_delete.get('requestObject[date]')
            date = ''.join(date)
            p= notification (therapist_username = therapist,patient_username=request.user,header='Cancel Appointment'
            ,message='the patient wants to cancel his appointment at '+date,description='you can contact the patient at',Unique_ID='8')
            p.save()


    else:
        return redirect('/portal/therapist')

# THERAPIST VIEWS #


def therapistDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        # the post request will contain Unique_ID, type (form/todo), action
        # status action: update status (read -- > unread)
        # delete action: delete the notification
        # confirm action: push the contents of the notification then delete// mark todo as complete and delete
        if request.method == "POST":
            from patientPortal.accessoryScripts.resourceManager import fixDict
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            request_dict = fixDict(request_dict)
            type = request_dict['type']
            action = request_dict['action']
            Unique_ID = request_dict['Unique_ID']
            if type == "notification":
                if action == "delete":
                    from patientPortal.modelHandlers.notifications import delete_notification
                    delete_notification(Unique_ID)

                elif action == "confirm":
                    from patientPortal.modelHandlers.notifications import handle_info_notification
                    handle_info_notification(Unique_ID)

                elif action == "status":
                    from patientPortal.modelHandlers.notifications import update_status
                    Unique_IDs = request_dict['Unique_ID']
                    update_statuses(Unique_IDs)

                else:
                    return HttpResponse(status=400) #Bad request

            elif type == "todo":
                if action == "delete":
                    from patientPortal.modelHandlers.todo import delete_todo
                    delete_todo(Unique_ID)
                if action =="create":
                    from patientPortal.modelHandlers.todo import create_todo
                else:
                    return HttpResponse(status=400)

            else:
                return HttpResponse(status=400) #Bad request

            return HttpResponse(status=200);

        # At this point all requests being made on this page are get requests
        from patientPortal.modelHandlers.todo import fetch_todos
        from patientPortal.modelHandlers.notifications import fetch_notifications
        notifications = fetch_notifications(request.user);

        # recall notification has patient_username, therapist_username,
        # unique_ID, header, message, description
        todos = fetch_todos(request.user);
        return render(request,'patientPortal/therapistDashboard.html',context={'notifications': notifications})
    else:
        return redirect('/portal/patient')


def therapistCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        patient_info = get_patient_info(request) # NOTE: kevin, this return patient info needed to populate therapist calendar
        return render_to_response('patientPortal/therapistCalendar.html')
    else:
        return redirect('/portal/patient')


def database(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        patient_info = get_patient_info(request) # NOTE: kevin, this returns a dict that contain all the info
        # needed to populate the database, just need to pass it to front end.

        return render_to_response('patientPortal/database.html')
    else:
        return redirect('/portal/patient')


def recruitment(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        from django.core.mail import send_mass_mail
        from patientPortal.apiScripts.exports import get_form_questions_from_params as data

        params = ['stroke','parkinson_s_disease','congestive_heart_failure','heart_attack']
        testdatum = data(params)
        testdatum = json.dumps(testdatum)
        #for i in testdatum:
        #    print(i)
        #print(testdatum);
        #data = script_to_get_question_info
        #data.stringy
        #for inside context--> 'data': data
        return render(request,'patientPortal/recruitment.html',context={'testdatum': testdatum})
    else:
        return redirect('/portal/patient')


def forms(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        from patientPortal.apiScripts.exports import get_available_forms
        method = request.method
        if (method == "GET"):
            request_query_dict = request.GET
            request_dict = dict(request_query_dict)
            if not bool(request_dict):  # The dict is empty means request has been made to load page
                forms = get_available_forms()
                return render(request, 'patientPortal/forms.html',  context={'forms': forms})

            # This call only needs to be done here, keeping it local
            from patientPortal.apiScripts.exports import get_form_groups

            # on JSON creation on front end, turns these values for the keys into lists
            # taking first element of the list fixes this issue

            form = request_dict['form'][0];
            event = request_dict['event'][0];
            question_groups = get_form_groups(form,event);
            response_body = {'question_groups': question_groups, 'event': event};
            return HttpResponse(json.dumps(response_body));

        if (method == "POST"):
            from patientPortal.apiScripts.imports import edit_patient_data_by_id
            from patientPortal.apiScripts.helper import create_redcap_event_name
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            request_dict = fixDict(request_dict);

            record_id = request_dict['record_id'];
            cohort_num = request_dict['cohort_num'];
            event_arm = request_dict['event_arm'];

            for key in ['record_id','cohort_num','event_arm','csrfmiddlewaretoken']:
                request_dict = removeDictKey(request_dict,key); # must remove the keys before passing to redcap api

            red_cap_event = create_redcap_event_name(event_arm,cohort_num);
            edit_patient_data_by_id(red_cap_event,record_id,request_dict);

            return HttpResponse(status=200);
    else:
        return redirect('/portal/patient')

def settings(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        return render_to_response('patientPortal/settings.html')
    else:
        return redirect('/portal/patient')

# FIXME must redirect to the appropriate dashboard


def dispatch(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        return redirect('/portal/patient')
    if is_therapist(request.user):
        return redirect('/portal/therapist')
    return redirect('/admin')
