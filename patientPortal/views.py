from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import MyPersonalInformationForm
# Create your views here.


def MyPersonalInformation(request):
    form = MyPersonalInformationForm(request.POST or None)
    if form. is_valid():
        save_it = form.save(commit=False)
        save_it.save()
    return render(request, 'patientPortal/information.html')


def myprogress(request):
    return render_to_response('patientPortal/myprogress.html')


def patientDashboard(request):
    return render_to_response('patientPortal/patientDashboard.html')

def exercise(request):
    return render_to_response('patientPortal/exercise.html')

def patientCalendar(request):
    return render_to_response('patientPortal/patientCalendar.html')
