from django.contrib import admin

# Register your models here.
from .models import information
class informationAdmin(admin.ModelAdmin):
    class Meta:
        model = information


admin.site.register(information, informationAdmin)
