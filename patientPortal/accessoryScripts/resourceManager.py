import copy;
def removeDictKey(dict, key):
    newDict = copy.deepcopy(dict)
    del newDict[key]
    return newDict;
def fixDict2(dict):
    for key in dict:
        if len(dict[key]) == 1:
            dict[key] = dict[key][0]
    return dict 
def fixDict(dict):
    from patientPortal.apiScripts.exports import get_all_questions
    questions = get_all_questions();
    checkbox_fields = [question['field_name'] for question in questions if question['field_type'] == 'checkbox']
    removed_checkboxes = [];
    added_keys = [];
    for key in dict:
        if len(dict[key]) == 1:
            dict[key] = dict[key][0]
        else:
            removed_checkboxes.append(key);
            for i in dict[key]:
                i = i.strip();
                newKey = key+"___"+i #In pycap check boxes are inputted with the name of the field_name,three underscores and the index of the options
                added_keys.append(newKey);
    for key in removed_checkboxes:
        dict = removeDictKey(dict,key)
    for key in added_keys:
        dict[key] = 1;
    return dict;
