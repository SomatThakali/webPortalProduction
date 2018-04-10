from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import MyPersonalInformationForm
from django.conf import settings
from django.shortcuts import redirect
from .accessoryScripts.checkGroup import is_patient, is_therapist
from django.http import HttpResponse

# PATIENT VIEWS #
def patientDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    if is_patient(request.user):
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        return render(
            request,'patientPortal/patientDashboard.html',context={'first_name': first_name, 'last_name': last_name},
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

            from patientPortal.apiScripts.exports import get_form_questions
            form = request_dict['form'];
            event = request_dict['event'];
            questions = get_form_questions
            return HttpResponse(simplejson.dumps(questions));
    else:
        return redirect('/portal/patient')

    #print(bool(request_dict))
    #forms = get_available_forms();
    #return render(request, 'patientPortal/forms.html',  context = {'forms' : forms})

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
