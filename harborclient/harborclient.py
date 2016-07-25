#!/usr/bin/env python

import requests
import simplejson


class HarborClient(object):
    def __init__(self, host, user, password, protocol="http"):
        self.host = host
        self.user = user
        self.password = password
        self.protocol = protocol

        self.session_id = self.login()

    def __del__(self):
        self.logout()

    def login(self):
        login_data = requests.post(
            '%s://%s/login' % (self.protocol, self.host),
            data={'principal': self.user,
                  'password': self.password})
        if login_data.status_code == 200:
            session_id = login_data.cookies.get('beegosessionID')

            print("Successfully login, session id: {}".format(session_id))
            return session_id
        else:
            print("Fail to login, please try again")
            return None

    def logout(self):
        requests.get('%s://%s/logout' % (self.protocol, self.host),
                     cookies={'beegosessionID': self.session_id})
        print("Successfully logout")

    # Get project id 
    def get_project_id_from_name(self, project_name):
        registry_data = requests.get(
            '%s://%s/api/projects?project_name=%s' %
            (self.protocol, self.host, project_name),
            cookies={'beegosessionID': self.session_id})
        if registry_data.status_code == 200 and registry_data.json():
            project_id = registry_data.json()[0]['project_id']
            print("Successfully get project id: {}, project name: {}".format(
                project_id, project_name))
            return project_id
        else:
            pritn("Fail to get project id from project name", project_name)
            return None

    # GET /search
    def search(self, query_string):
        result = None
        path = '%s://%s/api/search?q=%s' % (self.protocol, self.host,
                                            query_string)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get search result: {}".format(result))
        else:
            print("Fail to get search result")
        return result

    # GET /projects
    def get_projects(self, project_name=None, is_public=None):
        # TODO: support parameter
        result = None
        path = '%s://%s/api/projects' % (self.protocol, self.host)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get projects result: {}".format(result))
        else:
            print("Fail to get projects result")
        return result

    # HEAD /projects
    def check_project_exist(self, project_name):
        # TODO: need test
        result = None
        path = '%s://%s/api/projects?project_name=%s' % (
            self.protocol, self.host, project_name)
        response = requests.head(
            path, cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully check project exist, result: {}".format(
                result))
        else:
            print("Fail to check project exist")
        return result

    # POST /projects
    def create_project(self):
        # TODO
        pass

    # TODO: remove this
    def get_project_id(session_id, project_name):
        registry_data = requests.get('%s://%s/api/projects?project_name=%s' %
                                     (protocol, host, project_name),
                                     cookies={'beegosessionID': session_id})
        if registry_data.status_code == 200 and registry_data.json():
            project_id = registry_data.json()[0]['project_id']
            print("Successfully get project id: {}".format(project_id))
            # get image list
            registry_list_data = requests.get(
                '%s://%s/api/repositories?project_id=%s' %
                (protocol, host, project_id),
                cookies={'beegosessionID': session_id})
            if registry_list_data.status_code == 200:
                data = ['%s/%s' % (host, x) for x in registry_list_data.json()]
                print("Successfully get project info, data: {}".format(data))
                return data
            else:
                print(
                    "Fail to get project info, response status code: {}".format(
                        registry_list_data.status_code))

        return None

    # PUT /projects/{project_id}/publicity
    def set_project_private(self, project_name):

        project_id = self.get_project_id_from_name(project_name)

        # set project private
        set_request = requests.put(
            '%s://%s/api/projects/%s/publicity?project_id=%s' %
            (self.protocol, self.host, project_id, project_id),
            cookies={'beegosessionID': self.session_id},
            data=simplejson.dumps({'public': False}))
        if set_request.status_code == 200:
            print("Success to set project {} private".format(project_name))
        else:
            print("Fail to set project private")

    # TODO: implement these
    # POST /projects/{project_id}/logs/filter
    # GET /projects/{project_id}/members/
    # GET /projects/{project_id}/members/{user_id}

    # GET /statistics
    def get_statistics(self):
        result = None
        path = '%s://%s/api/statistics' % (self.protocol, self.host)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get statistics: {}".format(result))
        else:
            print("Fail to get statistics result")
        return result

    # GET /users
    def get_users(self, user_name=None):
        # TODO: support parameter
        result = None
        path = '%s://%s/api/users' % (self.protocol, self.host)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get users result: {}".format(result))
        else:
            print("Fail to get users result")
        return result 


    # POST /users

    # PUT /users/{user_id}

    # DELETE /users/{user_id} 
    def delete_user(self, user_id):
        # TODO: need test
        result = False
        path = '%s://%s/api/users/%s?user_id=%s' % (self.protocol, self.host, user_id, user_id)
        response = requests.delete(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = True
            print("Successfully delete user with id: {}".format(user_id))
        else:
            print("Fail to delete user with id: {}".format(user_id))
        return result

    # PUT /users/{user_id}/password
    def change_password(self):
        # TODO: need implement
        pass

    # PUT /users/{user_id}/sysadmin
    def promote_as_admin(self, user_id):
        # TODO: need test
        result = False
        path = '%s://%s/api/users/%s/sysadmin?user_id=%s' % (self.protocol, self.host, user_id, user_id)
        response = requests.put(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = True
            print("Successfully promote user as admin with id: {}".format(user_id))
        else:
            print("Fail to promote user as admin with id: {}".format(user_id))
        return result


    # GET /repositories
    def get_repositories(self, project_id, query_string=None):
        # TODO: support parameter
        result = None
        path = '%s://%s/api/repositories?project_id=%s' % (self.protocol, self.host, project_id)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get repositories with id: {}, result: {}".format(project_id, result))
        else:
            print("Fail to get repositories result with id: {}".format(project_id))
        return result

    # DELETE /repositories

    # Get /repositories/tags
    def get_repository_tags(self, repo_name):
        # TODO: need test
        result = None
        path = '%s://%s/api/repositories/tags?repo_name=%s' % (self.protocol, self.host, repo_name)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            print("Successfully get tag with repo name: {}, result: {}".format(repo_name, result))
        else:
            print("Fail to get tags with repo name: {}".format(repo_name))
        return result

    # GET /repositories/manifests

