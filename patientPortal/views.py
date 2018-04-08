from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import MyPersonalInformationForm
from django.conf import settings
from django.shortcuts import redirect


# PATIENT VIEWS #
def patientDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientDashboard.html')

def MyPersonalInformation(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    form = MyPersonalInformationForm(request.POST or None)
    if form. is_valid():
        save_it = form.save(commit=False)
        save_it.save()
    return render(request, 'patientPortal/information.html')

def myprogress(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/myprogress.html')

def exercise(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/exercise.html')

def patientCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientCalendar.html')

# THERAPIST VIEWS #
def therapistDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/therapistDashboard.html')

def therapistCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/therapistCalendar.html')

def database(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/database.html')

def recruitment(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/recruitment.html')

def forms(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/forms.html')

def settings(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/settings.html')



# FIXME must redirect to the appropriate dashboard
def dispatch(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientDashboard.html')
