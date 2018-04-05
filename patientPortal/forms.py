from django import forms

from .models import MyPersonalInformation


class MyPersonalInformationForm(forms.ModelForm):
    class Meta:
        model = MyPersonalInformation
        fields = '__all__'
