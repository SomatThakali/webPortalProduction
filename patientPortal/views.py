from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .accessoryScripts.checkGroup import is_patient, is_therapist
from. forms import MyPersonalInformationForm
from. forms import MyContactInformationForm
from django.forms.formsets import formset_factory
import json
from .models import notification
from .models import Todo
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
        MyContactInformationFormSet = formset_factory(MyContactInformationForm,
                                                      extra=3, min_num=2, validate_min=True)
        if request.method == 'POST':
            form = MyPersonalInformationForm(request.POST)
            formset = MyContactInformationFormSet(request.POST)
            if form.is_valid() and formset.is_valid():
                for inline_form in formset:
                    personal = form.save()
                    if inline_form.cleaned_data:
                        contact = inline_form.save(commit=False)
                        contact.username = personal
                        contact.save()
                        return redirect('/patientPortal/information')
        else:
            form = MyPersonalInformationForm()
            formset = MyContactInformationFormSet()
        return render_to_response('patientPortal/information.html',
                                  {'form': form,  'formset': formset})
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
            return HttpResponseRedirect('/portal/patient', {'todos': n1})

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
            form = request_dict['form'][0]
            event = request_dict['event'][0]
            question_groups = get_form_groups(form, event)
            print(len(question_groups))
            response_body = {'guestion_groups': question_groups, 'event': event}
            return HttpResponse(json.dumps(response_body))
    else:
        return redirect('/portal/patient')

    # print(bool(request_dict))
    # forms = get_available_forms();
    # return render(request, 'patientPortal/forms.html',  context = {'forms' : forms})


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
