def clean_appointment_list(appts):
    for i in range(len(appts)):
        date = appts[i]['date']
        year = str(date.year)
        month = str(date.month)
        if len(month) < 2:
            month = '0' + month
        day = str(date.day)
        if len(day) < 2:
            day = '0' + day
        date = [year,month,day] # list of ints
        appts[i]['date'] = '-'.join(date)

        time = appts[i]['time']
        hour = str(time.hour)
        minute = time.minute;
        minute = str(minute)
        if len(minute) == 1:
            minute = '0' + minute
        time = [hour,minute]
        appts[i]['time'] = ':'.join(time)
    return appts

def get_appointments(user,group):
    if group == 'patient':
        appointments = user.patient_appointments.values()
    elif group == 'therapist':
        appointments = user.therapist_appointments.values()
    appointments = list(appointments)
    appointments = clean_appointment_list(appointments)
    return appointments
