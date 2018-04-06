from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import MyPersonalInformationForm
from django.conf import settings
from django.shortcuts import redirect


# Create your views here.


def MyPersonalInformation(request):
    form = MyPersonalInformationForm(request.POST or None)
    if form. is_valid():
        save_it = form.save(commit=False)
        save_it.save()
    return render(request, 'patientPortal/information.html')

def myprogress(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/myprogress.html')

def patientDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientDashboard.html')

def exercise(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/exercise.html')

def patientCalendar(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientCalendar.html')

def dispatch(request):
    if not request.user.is_authenticated:
        return redirect('/portal/login')
    return render_to_response('patientPortal/patientDashboard.html')
