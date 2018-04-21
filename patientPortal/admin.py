from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MyPersonalInformation
from .models import MyContactInformation
from .models import appointment
from .models import notification
from .models import Todo
from .models import Study

# from .models import Users
#
#
# class UsersInline(admin.StackedInline):
#     model = Users
#     can_delete = False
#     verbose_name_plural = 'User'
#     # Define a new User admin
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (UsersInline, )
#
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


class MyPersonalInformationAdmin(admin.ModelAdmin):
    model = MyPersonalInformation
    verbose_name_plural = 'My_Personal_Information'
    list_display = ('username', 'First_Name',  'Last_Name')


admin.site.register(MyPersonalInformation, MyPersonalInformationAdmin)


class MyContactInformationAdmin(admin.ModelAdmin):
    model = MyContactInformation
    verbose_name_plural = 'My_Contact_Information'


admin.site.register(MyContactInformation, MyContactInformationAdmin)


class appointmentAdmin(admin.ModelAdmin):
    model = appointment


admin.site.register(appointment, appointmentAdmin)


class notificationAdmin(admin.ModelAdmin):
    model = appointment


admin.site.register(notification, notificationAdmin)


class TodoAdmin(admin.ModelAdmin):
    model = Todo
    verbose_name_plural = 'Todo'
    list_display = ('title', 'patient_username', 'completed',  'due_date')
    search_fields = ('title',)


admin.site.register(Todo, TodoAdmin)


class StudyAdmin(admin.ModelAdmin):
    model = Study
    verbose_name_plural = 'Study'
    list_display = ('title', 'therapist_username', 'researcher_name')
    search_fields = ('title', 'therapist_username')


admin.site.register(Study, StudyAdmin)
