def get_newest_cohort_data(patient):
    cohort_data = get_cohort_data(patient)
    newest_datum = cohort_data[len(cohort_data)-1]
    patient_id = newest_datum.record_id            #Gets the values from the newest input
    cohort_num = newest_datum.cohort_num
    cohort_data = {'record_id': patient_id, 'cohort_num': cohort_num}
    return cohort_data

def get_cohort_data(patient):
    cohort_data = patient.cohortdata_set.all();
    return cohort_data
