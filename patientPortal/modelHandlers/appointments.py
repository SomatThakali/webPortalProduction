from patientPortal.models import appointment
def appointment_happened(date, time):
    import datetime
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    if current_date > date:
        return True
    if current_date == date:
        if current_time > time:
            return True
    return False

def clean_appointment_list(appts):
    from django.contrib.auth.models import User
    future_appts = []
    past_appts = []
    for i in range(len(appts)):
        appt = appts[i]

        date = appt['date']
        appt['date'] = date.strftime("%Y-%m-%d")

        time = appt['time']
        appt['time'] = time.strftime("%H:%M")

        happened = appointment_happened(date,time)
        appt['patient_name'] = User.objects.get(id=appts[i]['patient_id']).first_name
        appt['therapist_name'] = User.objects.get(id=appts[i]['therapist_id']).first_name

        if happened:
            past_appts.append(appt)
        else:
            future_appts.append(appt)
    appts = {'past_appts': past_appts, 'future_appts': future_appts}
    return appts

def get_appointments(user,group):
    if group == 'patient':
        appointments = user.patient_appointments.values()
    elif group == 'therapist':
        appointments = user.therapist_appointments.values()
    appointments = list(appointments)
    appointments = clean_appointment_list(appointments)
    return appointments

def fetch_appointment(Unique_ID):
    n = appointment.objects.get(Unique_ID=Unique_ID);
    return n;
