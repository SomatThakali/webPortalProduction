from django.contrib.auth.models import User
from patientPortal.modelHandlers.appointments import get_appointments

def get_personal_info(request):
        p = User.objects.filter(username=request)[0] # this gets everything you want about the patient
        first_name = p.mypersonalinformation.First_Name
        last_name=p.mypersonalinformation.Last_Name
        email = p.mycontactinformation.email
        phone = p.mycontactinformation.Phone_Number
        address1 = p.mycontactinformation.Address_Line_2
        address2 = p.mycontactinformation.Address_Line_1
        DOB = p.mypersonalinformation.Date_of_Birth
        DOB=str(DOB.year)+'-'+str(DOB.month)+'-'+str(DOB.day)
        emergency_first =  p.mypersonalinformation.Emergency_Contact_Name
        emergency_phone =  p.mypersonalinformation.Emergency_Contact_Phone

        return  {'phone': phone,'email' :email, 'adline1':address1,'adline2':address2,
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

def get_study_info (request):
    from patientPortal.models import Study
    p = User.objects.filter(username=request)[0]
    s = Study.objects.get(therapist_username=p)
     #s.title

def get_patient_info(request):
    patient_info = {}
    from django.contrib.auth.models import User
    from patientPortal.models import CohortData, UserProfile
    therapist = User.objects.filter(username=request.user)[0]
    result = UserProfile.objects.filter(therapist_user=therapist) # NOTE: return the patients of the therapist
    for patient in range( len(result)):
        info = result[patient].user # get info of the patient
        username=info.username
    #    appointment = (request.user,'patient')
        first_name = info.first_name
        last_name = info.last_name
        patient_info [patient] = {'first_name':first_name,'last_name':last_name,
        }

    return patient_info
