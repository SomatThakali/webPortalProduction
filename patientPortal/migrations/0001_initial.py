# Generated by Django 2.0.3 on 2018-04-17 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affected_limb', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyContactInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone_Number', models.CharField(max_length=20)),
                ('Address_Line_1', models.CharField(max_length=40)),
                ('Address_Line_2', models.CharField(max_length=40)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyPersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=15)),
                ('Middle_Name', models.CharField(blank=True, max_length=15)),
                ('Last_Name', models.CharField(max_length=15)),
                ('Date_of_Birth', models.DateField()),
                ('Emergency_Contact_Name', models.CharField(max_length=30)),
                ('Emergency_Contact_Phone', models.CharField(max_length=20)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_username', models.CharField(blank=True, max_length=15)),
                ('Unique_ID', models.CharField(max_length=20, unique=True)),
                ('header', models.CharField(max_length=30)),
                ('message', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('viewed', models.BooleanField(default=False)),
                ('therapist_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_username', models.CharField(blank=True, max_length=15)),
                ('Unique_ID', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=140)),
                ('created_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('therapist_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='First_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='onrecord', to='patientPortal.MyPersonalInformation'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
