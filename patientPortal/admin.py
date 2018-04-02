from django.contrib import admin

# Register your models here.
from .models import login
from .models import information


class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = login


admin.site.register(login, SignUpAdmin)


class informationAdmin(admin.ModelAdmin):
    class Meta:
        model = information


admin.site.register(information, informationAdmin)
