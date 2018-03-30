from django.shortcuts import render
from django.shortcuts import render_to_response
from. forms import informationForm
# Create your views here.


def Signup(request):
    return render(request, 'patientPortal/Signup.html')


def information(request):
    form = informationForm(request.POST or None)
    if form. is_valid():
        save_it = form.save(commit=False)
        save_it.save()
    return render(request, 'patientPortal/information.html')


def myprogress(request):
    return render_to_response('patientPortal/myprogress.html')
