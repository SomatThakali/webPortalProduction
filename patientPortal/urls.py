from django.urls import include, path

from . import views

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('information',views.information),
    path('myprogress',views.myprogress),
    path('',views.patientDashboard),
]
