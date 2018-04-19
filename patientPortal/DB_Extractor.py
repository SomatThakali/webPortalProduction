# TODO what if u have multiple appointments (somat should fix mod first),
# what about pm am thing,
# how to delete.

from django.contrib.auth.models import User

def get_personal_info(request):
        p = User.objects.filter(username=request)[0] # this gets everything you want about the patient
        first_name=p.mypersonalinformation.First_Name
        last_name=p.mypersonalinformation.Last_Name
        email = p.mycontactinformation.email
        phone = p.mycontactinformation.Phone_Number
        address1 = p.mycontactinformation.Address_Line_2
        address2 = p.mycontactinformation.Address_Line_1
        DOB = p.mypersonalinformation.Date_of_Birth
        DOB=str(DOB.year)+'-'+str(DOB.month)+'-'+str(DOB.day)
        emergency_first =  p.mypersonalinformation.Emergency_Contact_Name
        emergency_phone =  p.mypersonalinformation.Emergency_Contact_Phone

        return  {'phone': phone,'email' :email, 'adline':address1,'adline2':address2,
        'DOB':DOB, 'emergency_first':emergency_first , 'emergency_phone':emergency_phone,
        'first_name':first_name,'last_name':last_name}


def get_apoint_info(request):
    p = User.objects.filter(username=request)[0]
    apointment=p.appointment
    day   = apointment.date.day
    month = apointment.date.month
    year  = apointment.date.year
    date = str(year)+'-'+ str(month)+'-'+str(day)

    hour = p.appointment.time.hour
    minute = p.appointment.time.minute
    time = str(hour)+':'+str(minute)
    
    return  {'date': date,'time':time,'apoint': apointment}
