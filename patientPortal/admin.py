from django.contrib import admin

# Register your models here.
from .models import MyPersonalInformation
from .models import MyContactInformation
from .models import MyEmergencyContact
from .models import appointment


class MyPersonalInformationAdmin(admin.ModelAdmin):
    class Meta:
        model = MyPersonalInformation


admin.site.register(MyPersonalInformation, MyPersonalInformationAdmin)


class MyContactInformationAdmin(admin.ModelAdmin):

    class Meta:

        model = MyContactInformation


admin.site.register(MyContactInformation, MyContactInformationAdmin)


class MyEmergencyContactAdmin(admin.ModelAdmin):
    class Meta:
        model = MyEmergencyContact


admin.site.register(MyEmergencyContact, MyEmergencyContactAdmin)


class appointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = appointment


admin.site.register(appointment, appointmentAdmin)
