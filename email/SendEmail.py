from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User

# get this front front end.
user_input='gtouchan94@gmail.com'
subject = 'Some subject'
from_email = settings.DEFAULT_FROM_EMAIL
message = 'This is my test message'
html_message = '<h1>This is my HTML test</h1>' # link to page to reset password
recipient_list = [user_input] # this comes from the user input.

# does the patient excist on our DB ?
p = User.objects.filter(email=user_input)
if p is not None:
    send_mail(subject, message, from_email, recipient_list,fail_silently=False, html_message=html_message)
