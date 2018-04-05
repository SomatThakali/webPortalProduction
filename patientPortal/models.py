from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime


# Create your models here.
class MyPersonalInformation(models.Model):
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15)
    birthday = models.DateField()
    RACE_CHOICES = (
        ('1', 'African Amercan'),
        ('2', 'Amercan Indian'),
        ('3', 'Asian'),
        ('4', 'Hispanic'),
        ('5', 'White'),
    )
    race = models.CharField(max_length=1, choices=RACE_CHOICES)

    GENDER_CHOICES = (
        ('1', 'Male'),
        ('2', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name


class MyContactInformation(models.Model):
    myPersonal = models.ForeignKey(MyPersonalInformation,
                                   on_delete=models.CASCADE,)
    phone_Number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=2)
    Zip_Code = models.CharField(max_length=5)


def __unicode__(self):
    return self.myPersonal


class MyEmergencyContact(models.Model):
    myPersonalInformation = models.ForeignKey(MyPersonalInformation,
                                              on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15)
    phone_Number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True)


def __str__(self):
    return self.myPersonalInformation


class appointManager(models.Manager):
    def appointval(self, postData, id):
        errors = []
        # print str(datetime.today()).split()[1]->
        #  to see just the time in datetime
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


class appointment(models.Model):
    user = models.ForeignKey(MyPersonalInformation, related_name="onrecord",
                             blank=True, null=True, on_delete=models.CASCADE,)
    affected_limb = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = appointManager()
