from django.urls import include, path

from . import views

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('patient/information',views.information),
    path('patient/myprogress',views.myprogress),
    path('patient',views.patientDashboard),
]
