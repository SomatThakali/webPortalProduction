def get_project():
    from redcap import Project
    URL = 'https://redcap.ctsc.weill.cornell.edu/redcap_protocols/api/'
    API_KEY = '2750CFFE8A32D7C3F4FAC80603CE74E6'
    project = Project(URL, API_KEY)
    #returns a project object, allows this to remain here
    return project;
