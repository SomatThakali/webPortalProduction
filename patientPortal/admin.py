from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MyPersonalInformation
from .models import MyContactInformation
from .models import MyEmergencyContact
from .models import appointment
from .models import Users


class UsersInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name_plural = 'User'
    # Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# admin.site.register(User, UserAdmin)


class MyPersonalInformationAdmin(admin.ModelAdmin):
    model = MyPersonalInformation


admin.site.register(MyPersonalInformation, MyPersonalInformationAdmin)


class MyContactInformationAdmin(admin.ModelAdmin):
    model = MyContactInformation


admin.site.register(MyContactInformation, MyContactInformationAdmin)


class MyEmergencyContactAdmin(admin.ModelAdmin):
    model = MyEmergencyContact


admin.site.register(MyEmergencyContact, MyEmergencyContactAdmin)


class appointmentAdmin(admin.ModelAdmin):
    model = appointment


admin.site.register(appointment, appointmentAdmin)
