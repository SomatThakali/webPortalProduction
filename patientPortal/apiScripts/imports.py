from apiCall import get_project

# changes is to be edited
def edit_patient_data_by_id(redcap_event_name,record_id,changes):
    project = get_project();
    changes['record_id'] = record_id;
    changes['redcap_event_name'] = redcap_event_name
    project.import_records([changes]);
