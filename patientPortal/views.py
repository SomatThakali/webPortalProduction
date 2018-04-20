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
from .DB_Extractor import get_personal_info, get_apoint_info
from. forms import MyPersonalInformationForm
from. forms import MyContactInformationForm
import json
from .models import notification
from .models import Todo
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
        if request.method == 'POST':
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            # TODO i included a form_type within the return dict to say personalInfo or contact to save in appropriate database
            print(request_dict)
            return HttpResponse({'success':"Successful submission"})

        from patientPortal.apiScripts.exports import get_specific_data_by_id
        from patientPortal.apiScripts.helper import create_redcap_event_name

        # TODO for these they need to come from the user object
        patient_id = 'testdcap4'
        cohort_num = '1'

        #This can remain hardcoded
        event_prefix = 'admin'
        redcap_event = create_redcap_event_name(event_prefix,cohort_num)
        fields_of_interest = ['name','contactphone','adline','adline2','dob','email','emergencycontact','emergencycontactnum']

        patient_data = get_specific_data_by_id(redcap_event,patient_id,fields_of_interest)
        return render(request, 'patientPortal/information.html', context = patient_data)
        
    else:
        return redirect('/portal/therapist')


def myprogress(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        return render_to_response('patientPortal/myprogress.html')
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
        request_query_dict = request.GET;
        request_dict = dict(request_query_dict);

        request_query_dict2 = request.POST;
        request_dict2 = dict(request_query_dict2);
        print(request_query_dict2)
        print(request_dict2)

        try:
            info=get_apoint_info(request.user)
        except ObjectDoesNotExist:
            pass

        # FIXME notice that this does two calls to the page on load. 1 to just load the page and 2 to transmit data
        # Must be better way of doing this, but seemed the most reasonable solution due to strang
        if bool(request_dict):
            #Filler information to test front end response
            therapist = "Some Guy"
            try:
                appts = [{'date' : info['date'], 'time':info['time']}]

            except UnboundLocalError: # if it is empty:
                appts = [{'date':'0000-00-00','time':'0:00pm'}]     

            response_body = {"therapist": therapist, "appts": appts}
            return HttpResponse(json.dumps(response_body));



        if bool(request_dict2):
            info['apoint'].delete()

        return render_to_response('patientPortal/patientCalendar.html')
    else:
        return redirect('/portal/therapist')

# THERAPIST VIEWS #


def therapistDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):

        def show_notifications(request, notifications_id):
            n = notification.objects.get(id=notifications_id)
            return render_to_response('patientPortal/therapistDashboard.html', {'notifications': n})

        def delete_notifications(request, notifications_id):
            n = notification.objects.get(id=notifications_id)
            n.viewed = True
            n.save()
            n1 = notification.objects.filter(user=request.user, viewed=False)
            return HttpResponseRedirect('/portal/patient', {'notifications': n1})

        def show_todos(request, todos_id):
            n = Todo.objects.get(id=todos_id)
            return render_to_response('patientPortal/therapistDashboard.html', {'todos': n})

        def delete_todos(request, todos_id):
            n = Todo.objects.get(id=todos_id)
            n.completed = True
            n.save()
            n1 = Todo.objects.filter(user=request.user, completed=False)
            # n1.delete() could be used to delete records.
            return HttpResponseRedirect('/portal/patient', {'todos': n1})

        notifications = [];
        notifications.append({'patient_name': 'John Doe','Unique_ID':'5162d31', 'header' :'Reschedule - John Doe','message': 'John Doe would like to reschedule his 2:00 PM therapy session','description':'reschedule','viewed':False});
        notifications.append({'patient_name': 'John Doe','Unique_ID':'5162d31', 'header' :'Reschedule - John Doe','message': 'John Doe would like to reschedule his 2:00 PM therapy session','description':'reschedule','viewed':False});
        notifications.append({'patient_name': 'John Doe','Unique_ID':'5162d31', 'header' :'Reschedule - John Doe','message': 'John Doe would like to reschedule his 2:00 PM therapy session','description':'reschedule','viewed':False});
        notifications.append({'patient_name': 'John Doe','Unique_ID':'5162d31', 'header' :'Reschedule - John Doe','message': 'John Doe would like to reschedule his 2:00 PM therapy session','description':'reschedule','viewed':False});
        notifications.append({'patient_name': 'John Doe','Unique_ID':'5162d31', 'header' :'Reschedule - John Doe','message': 'John Doe would like to reschedule his 2:00 PM therapy session','description':'reschedule','viewed':False});

        return render(request,'patientPortal/therapistDashboard.html',context={'notifications': notifications})
    else:
        return redirect('/portal/patient')


def therapistCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        return render_to_response('patientPortal/therapistCalendar.html')
    else:
        return redirect('/portal/patient')


def database(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        return render_to_response('patientPortal/database.html')
    else:
        return redirect('/portal/patient')


def recruitment(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        return render(request,'patientPortal/recruitment.html',context={})
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
            request_query_dict = request.POST;
            request_dict = dict(request_query_dict);
            record_id = request_dict['record_id'];
            cohort_num = request_dict['cohort_num'];
            event_arm = request_dict['event_arm'];
            from .accessoryScripts.resourceManager import removeDictKey, fixDict
            for key in ['record_id','cohort_num','event_arm','csrfmiddlewaretoken']:
                request_dict = removeDictKey(request_dict,key);
            print(request_dict);
            request_dict = fixDict(request_dict);
            print(request_dict);
            from patientPortal.apiScripts.imports import edit_patient_data_by_id
            from patientPortal.apiScripts.helper import create_redcap_event_name
            red_cap_event = create_redcap_event_name(event_arm[0],cohort_num[0]);
            edit_patient_data_by_id(red_cap_event,record_id[0],request_dict);

            return HttpResponse(json.dumps({'status': 'successful submission'}));
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
