from patientPortal.models import notification
from django.contrib.auth.models import User

# get request handler
def fetch_notifications(therapist_user):
    notification_list = therapist_user.notification_set.all();
    notifications = notification_list.values();
    print(notifications)
    return notifications
    # delete request handler
def delete_notification(Unique_ID):
    n = fetch_notification(Unique_ID);
    n.delete()
    #notification.delete();
    return

def update_status(Unique_ID):
    n = fetch_notification(Unique_ID);

    return

def update_statuses(Unique_IDs):
    for Unique_ID in Unique_IDs:
        update_status(Unique_ID);

def fetch_notification(Unique_ID):
    n = notification.objects.get(Unique_ID=Unique_ID);
    return n;

# contents will be a dictionary containing the contents for the notification
# will contain patient_username, therapist_username
# Unique_ID for Appointment
def create_appointment_notification(contents):
    patient_username = contents['patient_username'];
    therapist_username = contents['therapist_username'];
    
    return

# contents will be a dictionary containting the contents for the notification
# will contain the patient_username, therapist_username
# data_change, a dictionary that contains the redcap field_names as keys,
# the values will be a dictionary with old_value and new_value
def create_info_notification(contents):
    return

def handle_appointment_notification(action):
    return

def handle_info_notification(action):
    return

def perform_notification(Unique_ID):
    import json
    n = notification.objects.get(Unique_ID=Unique_ID);
    description = n.description; # we want description to be a string of a dictionary
    description = json.loads(description); # turns the description string into a python dictionary

    type = description['type']  # type will be either notification or todo
    action = description['action'] # action will be list of things that will need to occur
    if type == "notification":
        handle_info_notification(action)
    if type == "todo":
        handle_appointment_notification(action);

    print("WORKING")
    #delete_notification(unique_ID);
    return
