from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import appointment, notification, Todo, Study, UserProfile, CohortData

class UserAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = True
    fk_name='user'
    verbose_name_plural = 'User Profile'
    extra = 0

class CohortDataAdmin(admin.StackedInline):
    model = CohortData;
    extra = 0;
    can_delete = True
    verbose_name_plural = 'Cohort Data';

class UserProfileAdmin(BaseUserAdmin):
    inlines = [UserAdmin,CohortDataAdmin]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

class appointmentAdmin(admin.ModelAdmin):
    model = appointment
    #list_display = ('First_name', 'date')
    #search_fields = ('username', 'date', 'First_Name')

admin.site.register(appointment, appointmentAdmin)

class notificationAdmin(admin.ModelAdmin):
    model = appointment
    list_display = ('therapist_username', 'patient_username', 'Unique_ID', 'viewed')
    search_fields = ('Unique_ID', 'therapist_username', 'patient_username')


admin.site.register(notification, notificationAdmin)


class TodoAdmin(admin.ModelAdmin):
    model = Todo
    verbose_name_plural = 'Todo'
    list_display = ('title', 'patient_username', 'completed',  'due_date')
    search_fields = ('title', 'Unique_ID', 'therapist_username', 'patient_username')

admin.site.register(Todo, TodoAdmin)

class StudyAdmin(admin.ModelAdmin):
    model = Study
    verbose_name_plural = 'Study'
    list_display = ('title', 'therapist_username', 'researcher_name')
    search_fields = ('title', 'therapist_username')

admin.site.register(Study, StudyAdmin)
