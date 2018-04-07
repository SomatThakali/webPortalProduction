from apiCall import get_project

def get_forms_questions(form_name):
    project = get_project();
    if form_name not in project.forms:
        raise ValueError("Form does not exist");
    meta_data = project.metadata;

    form_questions_meta = [datum for datum in meta_data if datum['form_name']==form_name]
    #returns a list of questions within a certain form with important data for filling
    return form_questions_meta


#here event_prefix is either admin or dc
def get_event_data(redcap_event_name):
    project = get_project();
    all_data = project.export_records();
    event_data = [datum for datum in all_data if datum['redcap_event_name'] == redcap_event_name]

    #returns a list of all data entries within a field
    return event_data

def get_patient_data_by_id(redcap_event_name,record_id):
    event_data = get_event_data(event_name, cohort_num);

    patient = [daum for datum in event_data if datum['record_id'] == record_id][0];
    #returns all patient data
    return patient

"""
try:
    get_forms_questions('patient_demographics')
except ValueError as err:
    print(err)
"""
