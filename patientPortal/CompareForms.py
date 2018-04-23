 # TODO: once u get full redcap access, replace the word 'email' with the word field
# and you should be good to go.
def compare_info(patient_data,request_dict,fields_of_interest):
    for field in fields_of_interest:
        if ((((request_dict.get('email')))!=None) and ((patient_data['email'])!=None)):
            if ((patient_data['email'])!=(''.join(request_dict.get('email')))):
                return 'email' +' to ' + ''.join(request_dict.get('email'))
