from django import forms


class MyPersonalInformationForm(forms.Form):
    # username = forms.OneToOneField(User,
    #                                on_delete=models.CASCADE,)
    First_Name = forms.CharField(max_length=15)
    Middle_Name = forms.CharField(max_length=15)
    Last_Name = forms.CharField(max_length=15)
    Date_of_Birth = forms.DateField(widget=forms.SelectDateWidget)
    Emergency_Contact_Name = forms.CharField(max_length=20)
    Emergency_Contact_Phone = forms.CharField(max_length=20)


class MyContactInformationForm(forms.Form):
    Phone_Number = forms.CharField(max_length=20)
    Address_Line_1 = forms.CharField(max_length=40)
    Address_Line_2 = forms.CharField(max_length=40)
    email = forms.EmailField(max_length=50)
