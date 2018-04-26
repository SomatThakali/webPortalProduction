from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
# from django.conf import settings
# from django.contrib.auth.models import Group
from django.utils import timezone

# Class to store a users cohort and redcap identifying information (cohort number and record_id)
class CohortData(models.Model):
    cohort_num = models.CharField(max_length=1);
    record_id = models.CharField(max_length=15);
    user = models.ForeignKey("auth.User",limit_choices_to={'groups__name': 'patient'}, on_delete=models.CASCADE)
    # patient can have multiple of these records

class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", limit_choices_to={'groups__name': 'patient'}, on_delete=models.CASCADE,)
    therapist_user = models.ForeignKey(
        "auth.User", limit_choices_to={'groups__name': 'therapist'}, on_delete=models.CASCADE, related_name='therapist_user')

class appointManager(models.Manager):
    def appointval(self, postData, id):
        errors = []
        print(postData["time"])
        print(datetime.now().strftime("%H:%M"))
        if postData['date']:
            if not postData["date"] >= unicode(date.today()):
                errors.append("Date must be set in future!")
            if len(postData["date"]) < 1:
                errors.append("Date field can not be empty")
            print("got to appointment post Data:", postData['date'])
        if len(appointment.objects.filter(date=postData['date'],
                                          time=postData['time'])) > 0:
            errors.append("Can Not create an appointment on existing date and time")
        if len(postData['task']) < 2:
            errors.append("Please insert take, must be more than 2 characters")
        if len(errors) == 0:
            makeappoint = appointment.objects.create(user=MyPersonalInformation.objects.get(
                id=id), task=postData['task'], date=str(postData['date']),
                time=postData['time'])
            return(True, makeappoint)
        else:
            return(False, errors)

    def edit_appointment(self, postData, app_id):
        errors = []
        print(errors)
        # if postData['edit_date']:
        if not postData["edit_date"] >= unicode(date.today()):
            errors.append("Appointment date can't be in the past!")
            print("appoint date can't be past")
        if postData["edit_date"] == "" or len(postData["edit_tasks"]) < 1:
            errors.append("All fields must be filled out!")
            print("all fields must fill out pop out")
        if errors == []:
            update_time = self.filter(id=app_id).update(
                task=postData['edit_tasks'], status=postData['edit_status'],
                time=postData['edit_time'], date=postData['edit_date'])

            return (True, update_time)
        else:
            return (False, errors)

# Class to store appointment information
class appointment(models.Model):
    import uuid
    patient = models.ForeignKey("auth.User", limit_choices_to={'groups__name': 'patient'}, on_delete=models.CASCADE,related_name='patient_appointments')
    therapist = models.ForeignKey("auth.User", limit_choices_to={'groups__name': 'therapist'}, on_delete=models.CASCADE,related_name='therapist_appointments')
    affected_limb = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    Unique_ID = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = appointManager()

    def __str__(self):
        return self.patient.username

# Class to store notifications for therapists
class notification(models.Model):
    import uuid
    patient_username = models.CharField(max_length=15, blank=True)
    therapist_username = models.ForeignKey(User, on_delete=models.CASCADE)
    Unique_ID = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    header = models.CharField(max_length=30)
    message = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    viewed = models.BooleanField(default=False)

# Class to store todos for therapists
class Todo(models.Model):
    import uuid
    patient_username = models.CharField(max_length=15, blank=True)
    therapist_username = models.ForeignKey(User, on_delete=models.CASCADE)
    Unique_ID = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=140)
    created_date = models.DateField(default=timezone.now, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def overdue_status(self):
        "Returns whether the Tasks's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    # Auto-set the Task creation / completed date
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.now()
        super(Todo, self).save()

# Classto store study information
class Study (models.Model):
    therapist_username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True, null=True)
    researcher_name = models.CharField(max_length=15, blank=True)
    researcher_phone_number = models.CharField(max_length=15, blank=True)
    researcher_email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return self.title
