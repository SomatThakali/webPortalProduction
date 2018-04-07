def create_redcap_event_name(event_prefix, cohort_num):
    arr = [event_prefix, 'arm',str(cohort_num)]
    redcap_event_name = ".".join(arr)
    return redcap_event_name
