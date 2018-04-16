from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import MyPersonalInformationForm
from django.conf import settings
from django.shortcuts import redirect
from .accessoryScripts.checkGroup import is_patient, is_therapist
from django.http import HttpResponse
import json
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
        form = MyPersonalInformationForm(request.POST or None)
        if form. is_valid():
            save_it = form.save(commit=False)
            save_it.save()
        return render(request, 'patientPortal/information.html')
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


def patientCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        import json
        request_query_dict = request.GET;
        request_dict = dict(request_query_dict);

        # FIXME notice that this does two calls to the page on load. 1 to just load the page and 2 to transmit data
        # Must be better way of doing this, but seemed the most reasonable solution due to strang
        if bool(request_dict):

            #Filler information to test front end response
            therapist = "Some Guy"
            appts = [{'date' : '2018-04-14', 'time':'2:00pm'}, {'date':'2018-04-16','time':'3:00pm'}]
            # This part will remain the same
            response_body = {"therapist": therapist, "appts": appts}
            return HttpResponse(json.dumps(response_body));
        return render_to_response('patientPortal/patientCalendar.html')
    else:
        return redirect('/portal/therapist')

# THERAPIST VIEWS #


def therapistDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        return render_to_response('patientPortal/therapistDashboard.html')
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
        return render_to_response('patientPortal/recruitment.html')
    else:
        return redirect('/portal/patient')


def forms(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_therapist(request.user):
        from patientPortal.apiScripts.exports import get_available_forms
        method = request.method;
        if (method == "GET"):
            request_query_dict = request.GET;
            request_dict = dict(request_query_dict);
            if not bool(request_dict): # The dict is empty means request has been made to load page
                forms = get_available_forms();
                return render(request, 'patientPortal/forms.html',  context = {'forms' : forms})

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
            for key in ['record_id','cohort_num','event_arm','csrfmiddlewaretoken','handedness','stroketype','lesionloc','affectedsidebody','weaklimb','diagnostic_testing','program_of_interest','time']:
                request_dict = removeDictKey(request_dict,key);

            request_dict = fixDict(request_dict);

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
