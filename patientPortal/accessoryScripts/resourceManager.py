import copy;
def removeDictKey(dict, key):
    newDict = copy.deepcopy(dict)
    del newDict[key]
    return newDict;

def fixDict(dict):
    for key in dict:
        if len(dict[key]) == 1:
            dict[key] = dict[key][0]

    return dict;
