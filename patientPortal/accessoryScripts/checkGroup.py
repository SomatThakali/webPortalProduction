from django.contrib.auth.models import User, Group

def is_patient(user):
    return user.groups.filter(name="patient").exists();

def is_therapist(user):
    return user.groups.filter(name="therapist").exists();
