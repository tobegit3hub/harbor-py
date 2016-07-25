import requests
import simplejson


# Set project private
def set_project_private(host, user, password, project_name, protocol='http'):
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
        project_id = registry_data.json()[0]['project_id']

        # set project private
        set_request = requests.put(
            '%s://%s/api/projects/%s/publicity?project_id=%s' %
            (protocol, host, project_id, project_id),
            cookies={'beegosessionID': session_id},
            data=simplejson.dumps({'public': False}))
        if set_request.status_code == 200:
            print("Success to set project {} private".format(project_id))
        else:
            print("Fail to set project private")

    # logout
    requests.get('%s://%s/logout' % (protocol, host),
                 cookies={'beegosessionID': session_id})


set_project_private("10.69.1.246", "admin", "Harbor12345", "library")
