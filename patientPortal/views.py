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
import json
from .models import notification, Todo, appointment
from .accessoryScripts.resourceManager import fixDict, fixDict2, removeDictKey
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
            request_dict = fixDict2(request_dict);
            request_dict = removeDictKey(request_dict, 'csrfmiddlewaretoken')
            request_dict = removeDictKey(request_dict, 'form_type')  #TODO remove this from the front end request

            changes = compare_info(patient_data, request_dict) # we dont need fields_of_interest as a param here
            create_info_notification(therapist, request.user, changes)
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
            past_appts = appts['past_appts']
            future_appts = appts['future_appts']
            for appt in past_appts:
                print(appt['date'])
                month = int(appt['date'].split('-')[1])
                month = calendar.month_name[month]
                if month not in months:
                    months[month] = 1
                else:
                    months[month] += 1
            appts_left = len(future_appts)
            appts_attended = len(past_appts)
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
        from patientPortal.modelHandlers.notifications import create_appointment_notification
        request_query_dict = request.POST;
        request_query = dict(request_query_dict);
        request_query = fixDict2(request_query)
        create_appointment_notification(request_query['Unique_ID'],request_query['action'])


        return HttpResponse(status=200)
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
        # delete action: delete the notification
        # confirm action: push the contents of the notification then delete// mark todo as complete and delete
        if request.method == "POST":
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            request_dict = fixDict2(request_dict)
            type = request_dict['type']
            action = request_dict['action']
            Unique_ID = request_dict['Unique_ID']
            if type == "notification":
                if action == "delete":
                    from patientPortal.modelHandlers.notifications import delete_notification
                    delete_notification(Unique_ID)

                elif action == "confirm":
                    from patientPortal.modelHandlers.notifications import dispatch_notification
                    dispatch_notification(Unique_ID)
                    #from patientPortal.modelHandlers.notifications import handle_info_notification
                    #handle_info_notification(Unique_ID)

                else:
                    return HttpResponse(status=400) #Bad request
                return HttpResponse(status=200) # Good Request

            elif type == "todo":
                if action == "complete":
                    from patientPortal.modelHandlers.todo import delete_todo
                    delete_todo(Unique_ID)
                elif action =="create":
                    from patientPortal.modelHandlers.todo import create_todo
                else:
                    return HttpResponse(status=400) # Bad Request
                return HttpResponse(status=200) #Good Request

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
        return render(request,'patientPortal/therapistDashboard.html',context={'notifications': notifications, 'todos': todos})
    else:
        return redirect('/portal/patient')


def therapistCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        if request.method == "GET":
            request_query_dict = request.GET
            request_dict = dict(request_query_dict)
            request_dict = fixDict2(request_dict)
            if not bool(request_dict):  # The request is empty
                return render(request,'patientPortal/therapistCalendar.html',context={})
            else:
                from patientPortal.modelHandlers.appointments import get_appointments
                appointments = get_appointments(request.user,'therapist')
                patients = User.objects.filter(groups__name = 'patient')
                patient_names = [x.last_name + ', ' + x.first_name for x in patients]
                #Patients are all patients in the database, not just for that therapist

                return HttpResponse(json.dumps({'appts':appointments, 'patient_names': patient_names}))

        # Here only the post request
        from patientPortal.modelHandlers.appointments import get_appointments
        request_query_dict = request.POST
        request_dict = dict(request_query_dict)
        request_dict = fixDict2(request_dict)

        patient_name = request_dict['patient'] # format is last_name , first_name
        patientArr = patient_name.split(',')
        patientFirstName = patientArr[1].strip()
        patientLastName = patientArr[0].strip()

        therapist = request.user
        patient = User.objects.filter(groups__name = 'patient', first_name=patientFirstName, last_name = patientLastName)[0]
        #this will hopefully be only 1 person, will cause errors if two patients with same name
        import datetime as dt

        datetime = request_dict['datetime']    # format is Mon Apr 23 2018 12:00:00 GMT-0400 (EDT)
        datetimeArr = datetime.split()  #      ['Mon, Apr, 23, 2018, 12:00:00']
        timeStr = datetimeArr[4]
        datetimeTimeObj = dt.datetime.strptime(timeStr, '%H:%M:%S').time()
        dateStr =  ' '.join(datetimeArr[1:4])
        dateTimeDateObj = dt.datetime.strptime(dateStr, '%b %d %Y').date()

        # check if patient has appointments
        appointments = list(patient.patient_appointments.values())
        if len(appointments) == 0 :
            #No appointments
            # This should be done a better way
            forms_to_do = ['Fugl Meyer','Patient Demographics', 'Sf36 Questionnaire','Stroke Impact Scale','Box and Blocks','Gripstrength','Tally']
            for form in forms_to_do:
                title = "Complete " + form + " for " + patient.first_name + " " + patient.last_name
                message = "It is " + patient.first_name + " " + patient.last_name + " first session. The " + form + " should be filled out for RedCap. Complete on the Forms page."
                due_date = dateTimeDateObj
                t = Todo(patient_username = patient.username, therapist_username = therapist, title = title, due_date = dateTimeDateObj, message= message)
                t.save()

        a = appointment(patient =patient, therapist = therapist, description = "appointment", date = dateTimeDateObj, time = datetimeTimeObj)
        a.save()

        return HttpResponse(status=200)

    else:
        return redirect('/portal/patient')


def database(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        patients = User.objects.filter(groups__name = 'patient')
        patient_data = []
        for patient in patients:
            from patientPortal.modelHandlers.users import get_newest_cohort_data
            cohortData = get_newest_cohort_data(patient)
            patient_datum = {'first_name': patient.first_name, 'last_name': patient.last_name, 'email': patient.email, 'cohort_num' : cohortData['cohort_num'] ,'record_id':cohortData['record_id']}
            patient_data.append(patient_datum)
        print(patient_data)
        return render(request, 'patientPortal/database.html', context= {'patients':patient_data})
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
        from .modelHandlers.users import get_newest_cohort_data
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

            patients = User.objects.filter(groups__name = 'patient')
            patient_data = []
            for patient in patients:
                patient_name = patient.first_name + " " + patient.last_name
                cohort_data = get_newest_cohort_data(patient)
                record_id = cohort_data['record_id']
                patient_data.append({'record_id': record_id, 'name': patient_name})


            response_body = {'question_groups': question_groups, 'event': event, 'patients' : patient_data};
            return HttpResponse(json.dumps(response_body));

        if (method == "POST"):
            from patientPortal.apiScripts.imports import edit_patient_data_by_id
            from patientPortal.apiScripts.helper import create_redcap_event_name
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            request_dict = fixDict(request_dict);
            print(request_dict)
            full_name = request_dict['patient_name'].split()
            first_name = full_name[0]
            last_name = full_name[len(full_name)-1]
            patient = User.objects.filter(groups__name = 'patient', first_name=first_name, last_name = last_name)[0]
            cohort_data = get_newest_cohort_data(patient)
            record_id = cohort_data['record_id'];
            cohort_num = cohort_data['cohort_num'];
            event_arm = request_dict['event_arm'];

            # These keys wouldnt be in the redcap event so art to be removed
            for key in ['patient_name','event_arm','csrfmiddlewaretoken']:
                request_dict = removeDictKey(request_dict,key); # must remove the keys before passing to redcap api

            red_cap_event = create_redcap_event_name(event_arm,cohort_num);
            edit_patient_data_by_id(red_cap_event,record_id,request_dict);
            print("This is getting here")
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
