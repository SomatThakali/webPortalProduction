# Generated by Django 2.0.3 on 2018-03-31 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patientPortal', '0003_information'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SignUp',
            new_name='login',
        ),
    ]
