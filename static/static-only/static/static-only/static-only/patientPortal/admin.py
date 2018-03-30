from django.contrib import admin

# Register your models here.
from .models import SignUp
from .models import information


class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = SignUp


admin.site.register(SignUp, SignUpAdmin)


class informationAdmin(admin.ModelAdmin):
    class Meta:
        model = information


admin.site.register(information, informationAdmin)
