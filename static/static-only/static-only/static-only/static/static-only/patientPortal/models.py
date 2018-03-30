from django.db import models


# Create your models here.


class SignUp(models.Model):
    patient_ID = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=15, null=True, blank=True)

    def __unicode__(self):
        return str(self.email)


class information(models.Model):
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    birthday = models.DateTimeField()
    country = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name
