from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dispatch),
    path('patient', views.patientDashboard),
    path('patient/information', views.MyPersonalInformation),
    path('patient/myprogress', views.myprogress),
    path('patient/exercise',views.exercise),
    path('patient/calendar',views.patientCalendar),

    path('therapist', views.therapistDashboard),
    path('therapist/calendar', views.therapistCalendar),
    path('therapist/database', views.database),
    path('therapist/recruitment', views.recruitment),
    path('therapist/forms', views.forms),
    path('therapist/settings', views.settings),

]
