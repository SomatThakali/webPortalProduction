 # TODO: once u get full redcap access, replace the word 'email' with the word field
# and you should be good to go.
def compare_info(patient_data,request_dict):
    changes = {}
    test_data = {'name':'Somebody','contactphone':'2313226252', 'adline': '24 Somewhere Lane', 'adline2': 'Apt 4e', 'dob':'2008-12-02','emergencycontact':'Someone Else','emergencycontactnum':'2425213232'}
    for key in request_dict:
        try:
            old_data = patient_data[key]
        except KeyError:
            old_data = test_data[key]
        new_data = request_dict[key]
        if old_data != new_data:
            changes[key] = {'old_data': old_data, 'new_data': new_data}
    return changes
