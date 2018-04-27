from patientPortal.models import notification
from django.contrib.auth.models import User

# get request handler
def fetch_notifications(therapist_user):
    notification_list = therapist_user.notification_set.all();
    notifications = notification_list.values();
    return notifications
    # delete request handler
def delete_notification(Unique_ID):
    n = fetch_notification(Unique_ID);
    n.delete()
    return

def fetch_notification(Unique_ID):
    n = notification.objects.get(Unique_ID=Unique_ID);
    return n;

# contents will be a dictionary containing the contents for the notification
# will contain patient_username, therapist_username
# Unique_ID for Appointment

# Change can be a date object or will be 'cancel'
def create_appointment_notification(appointment_ID,change):
    from patientPortal.modelHandlers.appointments import fetch_appointment
    from json import dumps
    appt = fetch_appointment(appointment_ID)
    therapist = appt.therapist
    patient = appt.patient
    patient_full_name = patient.first_name + " " + patient.last_name
    header = patient_full_name + ": Request to Cancel Appointment"

    time = appt.time
    time_str = str(time.hour) + ":" + str(time.minute)
    message = message = patient_full_name + " would like to " + change + " their appointment for " + appt.date.strftime("%Y-%m-%d") + " at " + appt.time.strftime("%I:%M %p") + "."
    description = {'Unique_ID': appointment_ID,'action':change}

    description = dumps(description)
    n = notification(therapist_username = therapist, patient_username = patient.username, header=header, description=description, message=message)
    n.save()
    return

# contents will be a dictionary containting the contents for the notification
# will contain the patient_username, therapist_user
# data_changes, a dictionary that contains the redcap field_names as keys,
# the values will be a dictionary with old_value and new_value
def create_info_notification(therapist, patient, data_changes):
    from patientPortal.modelHandlers.users import get_newest_cohort_data
    from json import dumps
    cohort_data = get_newest_cohort_data(patient)
    patient_id = cohort_data['record_id']
    cohort_num = cohort_data['cohort_num']

    patient_full_name = patient.first_name + ' ' + patient.last_name
    header = patient_full_name + ' Updated Their Data'

    message = ""
    description = {'patient_id': patient_id, 'cohort_num': cohort_num, 'changes':{}}
    for key in data_changes:
        old_data = data_changes[key]['old_data']
        new_data = data_changes[key]['new_data']
        message += (key + ' changed from ' + old_data + ' to ' + new_data + '\n');
        description['changes'][key] = new_data
    description = dumps(description)

    n = notification(therapist_username = therapist, patient_username = patient.username, header=header, description=description, message=message)
    n.save()
    return

def dispatch_notification(Unique_ID):
    from json import loads
    n = fetch_notification(Unique_ID);
    description = n.description;
    if 'Unique_ID' in loads(description):
        handle_appointment_notification(n)
    else:
        handle_info_notification(n)

def handle_appointment_notification(notification_object):
    from json import loads
    from patientPortal.modelHandlers.appointments import fetch_appointment
    description = notification_object.description;
    action = loads(description)
    appointment_ID = action['Unique_ID']
    a = fetch_appointment(appointment_ID)
    action = action['action']
    if action == 'cancel':
        a.delete()
    else:
        # Create Todo
    notification_object.delete()

def handle_info_notification(notification_object):
    from json import loads
    from patientPortal.apiScripts.helper import create_redcap_event_name
    from patientPortal.apiScripts.imports import edit_patient_data_by_id
    description = notification_object.description
    action = loads(description);
    patient_id = action['patient_id']
    cohort_num = action['cohort_num']
    changes = action['changes']

    # OK to hard code as the initial patient form data
    event_prefix = 'admin'
    redcap_event_name = create_redcap_event_name(event_prefix,cohort_num)
    edit_patient_data_by_id(redcap_event_name,patient_id,changes)
    delete_notification(Unique_ID)
    return
