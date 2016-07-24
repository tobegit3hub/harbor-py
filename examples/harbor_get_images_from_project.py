import requests


# Get images from the project
def get_registry_image_list(host,
                            user,
                            password,
                            project_name,
                            protocol='http'):
    ''' get registry image list '''
    data = []
    # get session id
    login_data = requests.post(
        '%s://%s/login' % (protocol, host),
        data={'principal': user,
              'password': password})
    if login_data.status_code == 200:
        session_id = login_data.cookies.get('beegosessionID')
    else:
        return []

    # get project id
    registry_data = requests.get('%s://%s/api/projects?project_name=%s' %
                                 (protocol, host, project_name),
                                 cookies={'beegosessionID': session_id})
    if registry_data.status_code == 200 and registry_data.json():
        #import ipdb;ipdb.set_trace()
        project_id = registry_data.json()[0]['project_id']
        # get image list
        registry_list_data = requests.get(
            '%s://%s/api/repositories?project_id=%s' %
            (protocol, host, project_id),
            cookies={'beegosessionID': session_id})
        if registry_list_data.status_code == 200:
            data = ['%s/%s' % (host, x) for x in registry_list_data.json()]

    # logout
    requests.get('%s://%s/logout' % (protocol, host),
                 cookies={'beegosessionID': session_id})
    return data


projects = get_registry_image_list("10.69.1.246", "admin", "Harbor12345",
                                   "library")
print(projects)
