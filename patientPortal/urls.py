from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('patient/information', views.MyPersonalInformation),
    path('patient/myprogress', views.myprogress),
    path('patient/exercise',views.exercise),
    path('patient/patientcalendar',views.patientCalendar),
    path('patient', views.patientDashboard),

]
