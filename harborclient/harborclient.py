#!/usr/bin/env python

import json
import logging
import requests
import argparse

logging.basicConfig(level=logging.DEBUG)


class HarborClient(object):
    def __init__(self, host, user, password, protocol="http", verify_ssl_cert=True):
        self.host = host
        self.user = user
        self.password = password
        self.protocol = protocol
        self.based_url = '{}://{}'.format(self.protocol, self.host)
        self.verify_ssl_cert = verify_ssl_cert

        self.session_id = self.login()

    def __del__(self):
        self.logout()

    def login(self):
        login_url = '{}/login'.format(self.based_url)
        data = {'principal': self.user, 'password': self.password}
        login_data = requests.post(url=login_url, data=data, verify=self.verify_ssl_cert)

        if login_data.status_code == 200:
            session_id = login_data.cookies.get('beegosessionID')

            logging.debug('Successfully login, session id: {}'.format(session_id))
            return session_id
        else:
            logging.error('Failed to login, please try again')
            return None

    def logout(self):
        logout_url = '{}/log_out'.format(self.based_url)
        requests.get(url=logout_url, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        logging.debug("Successfully logout")

    def get_project_id_by_name(self, project_name):
        """
        GET /api/projects?project_name={}
        Get project id by its name
        :param project_name: Name of project
        :return:
        """
        path = '{}://{}/api/projects?project_name={}'.format(self.protocol, self.host, project_name)
        registry_data = requests.get(path, cookies={'beegosessionID': self.session_id},
                                     verify=self.verify_ssl_cert)

        if registry_data.status_code == 200 and registry_data.json():
            project_id = registry_data.json()[0]['project_id']
            logging.debug('Successfully get project id: {}, project name: {}'.format(project_id,
                                                                                     project_name))
            return project_id
        else:
            logging.error("Fail to get project id from project name",
                          project_name)
            return None

    # GET /search
    def search(self, query_string):
        result = None
        path = '{}://{}/api/search?q={}'.format(self.protocol, self.host,
                                                query_string)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get search result: {}'.format(result))
        else:
            logging.error('Failed to get search result')
        return result

    # GET /projects
    def get_projects(self, is_public=True):
        result = None
        projects_path = '{}/api/projects'.format(self.based_url)
        path = '{}?is_public={}'.format(projects_path, 1 if is_public else 0)
        response = requests.get(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get projects result: {}'.format(result))
        else:
            logging.error("Failed to get projects result")
        return result

    def check_project_exists(self, project_name):
        """
        HEAD /projects
        Check if the project name user provided already exists.
        :param project_name: Project name for checking exists.
        :return: True if project exists
        """
        result = False
        path = '{}://{}/api/projects?project_name={}'.format(self.protocol, self.host, project_name)
        response = requests.head(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = True
            logging.debug('Successfully check project existence, result: {}'.format(result))
        elif response.status_code == 401:
            result = False
            logging.info('Need to be logged in.')
        elif response.status_code == 404:
            result = False
            logging.debug('Successfully check project exist, result: {}'.format(result))
        else:
            logging.error('Failed to check project existence')
        return result

    def create_project(self, project_name, is_public=False):
        """
        POST /projects
        Create a new project
        :param project_name: New created project
        :param is_public: Create public project
        :return: True if created
        """
        result = False
        path = '{}://{}/api/projects'.format(self.protocol, self.host)
        # TODO: make metadata parameters configurable
        request_body = json.dumps({'project_name': project_name,
                                   'metadata': {
                                       'public': str(is_public).lower(),
                                       'enable_content_trust': 'true',
                                       'prevent_vul': 'true',
                                       'severity': 'critical',
                                       'auto_scan': 'true'}
                                   })

        print(request_body)

        response = requests.post(path, cookies={'beegosessionID': self.session_id},
                                 data=request_body, verify=self.verify_ssl_cert)

        if response.status_code == 201:
            result = True
            logging.debug('Successfully create project with project name: {}'.format(project_name))
        elif response.status_code == 400:
            result = False
            logging.info('Unsatisfied with constraints of the project creation.')
        elif response.status_code == 401:
            result = False
            logging.info('Need to be logged in.')
        elif response.status_code == 409:
            result = False
            logging.info('Project name already exists.')
        elif response.status_code == 415:
            result = False
            logging.error('Incorrect request data format.')
        else:
            logging.error('Failed to create project with project name: {}, response code: {}.'.format(
                    project_name, response.status_code))
        return result

    def get_project_detailed_info(self, project_id):
        """
        GET /projects/project_id
        This endpoint returns specific project information by project ID.
        :param project_id: Project ID for filtering results.
        :return: info about project
        """
        path = '{}://{}/api/projects/{}'.format(self.protocol, self.host, project_id)
        response = requests.get(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get projects result: {}'.format(result))
            return result
        elif response.status_code == 401:
            logging.info('Need to be logged in.')
        else:
            logging.error('Failed to get project detailed info')

    def delete_project(self, project_id):
        """
        DELETE /projects/project_id
        This endpoint returns specific project information by project ID.
        :param project_id: Project ID for filtering results.
        :return: True if project is deleted
        """
        path = '{}://{}/api/projects/{}'.format(self.protocol, self.host, project_id)
        response = requests.delete(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            logging.info('Project is deleted successfully.')
            return True
        if response.status_code == 400:
            logging.error('Project is deleted successfully.')
        elif response.status_code == 401:
            logging.info('Need to be logged in.')
        elif response.status_code == 404:
            logging.info('Project does not exist.')
        elif response.status_code == 412:
            logging.info('Project contains policies, can not be deleted.')
        else:
            logging.error('Failed to delete project')
        return False

    # GET /statistics
    def get_statistics(self):
        result = None
        path = '{}://{}/api/statistics'.format(self.protocol, self.host)
        response = requests.get(path,
                                cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get statistics: {}'.format(result))
        else:
            logging.error('Failed to get statistics result')
        return result

    # GET /users
    def get_users(self, user_name=None):
        # TODO: support parameter
        result = None
        path = '{}://{}/api/users'.format(self.protocol, self.host)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get users result: {}'.format(result))
        else:
            logging.error("Failed to get users result")
        return result

    # POST /users
    def create_user(self, username, email, password, realname, comment):
        result = False
        path = '{}://{}/api/users'.format(self.protocol, self.host)
        request_body = json.dumps({'username': username,
                                   'email': email,
                                   'password': password,
                                   'realname': realname,
                                   'comment': comment})
        response = requests.post(path, cookies={'beegosessionID': self.session_id},
                                 data=request_body)

        if response.status_code == 201:
            result = True
            logging.debug('Successfully create user with username: {}'.format(username))
        else:
            logging.error('Failed to create user with username: {}, response code: {}'.format(username,
                                                                                              response.status_code))
        return result

    # PUT /users/{user_id}
    def update_user_profile(self, user_id, email, realname, comment):
        # TODO: support not passing comment
        result = False
        path = '{}://{}/api/users/{}?user_id={}'.format(self.protocol, self.host,
                                                        user_id, user_id)
        request_body = json.dumps({'email': email,
                                   'realname': realname,
                                   'comment': comment})
        response = requests.put(path, cookies={'beegosessionID': self.session_id},
                                data=request_body)
        if response.status_code == 200:
            result = True
            logging.debug('Successfully update user profile with user id: {}'.format(user_id))
        else:
            logging.error('Failed to update user profile with user id: {}, response code: {}'.format(user_id,
                                                                                                     response.status_code))
        return result

    # DELETE /users/{user_id}
    def delete_user(self, user_id):
        result = False
        path = '{}://{}/api/users/{}?user_id={}'.format(self.protocol, self.host,
                                                        user_id, user_id)
        response = requests.delete(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = True
            logging.debug('Successfully delete user with id: {}'.format(user_id))
        else:
            logging.error('Failed to delete user with id: {}'.format(user_id))
        return result

    # PUT /users/{user_id}/password
    def change_password(self, user_id, old_password, new_password):
        result = False
        path = '{}://{}/api/users/{}/password?user_id={}'.format(self.protocol, self.host,
                                                                 user_id, user_id)
        request_body = json.dumps({'old_password': old_password,
                                   'new_password': new_password})
        response = requests.put(path, cookies={'beegosessionID': self.session_id}, data=request_body)

        if response.status_code == 200:
            result = True
            logging.debug('Successfully change password for user id: {}'.format(user_id))
        else:
            logging.error('Failed to change password for user id: {}'.format(user_id))
        return result

    # PUT /users/{user_id}/sysadmin
    def promote_as_admin(self, user_id):
        # TODO: always return 404, need more test
        result = False
        path = '{}://{}/api/users/{}/sysadmin?user_id={}'.format(self.protocol, self.host,
                                                                 user_id, user_id)
        response = requests.put(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = True
            logging.debug('Successfully promote user as admin with user id: {}'.format(user_id))
        else:
            logging.error('Failed to promote user as admin with user id: {}, response code: {}'.format(
                user_id, response.status_code))
        return result

    # GET /repositories
    def get_repositories(self, project_id, query_string=None):
        # TODO: support parameter
        result = None
        path = '{}://{}/api/repositories?project_id={}'.format(self.protocol, self.host,
                                                               project_id)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get repositories with id: {}, result: {}'.format(project_id, result))
        else:
            logging.error('Failed to get repositories result with id: {}'.format(project_id))
        return result

    # DELETE /repositories
    def delete_repository(self, repo_name, tag=None):
        # TODO: support to check tag
        # TODO: return 200 but the repo is not deleted, need more test
        result = False
        path = '{}://{}/api/repositories?repo_name={}'.format(self.protocol, self.host, repo_name)
        response = requests.delete(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = True
            logging.debug('Successfully delete repository: {}'.format(repo_name))
        else:
            logging.error('Failed to delete repository: {}'.format(repo_name))
        return result

    # Get /repositories/tags
    def get_repository_tags(self, repo_name):
        result = None
        path = '{}://{}/api/repositories/tags?repo_name={}'.format(self.protocol, self.host, repo_name)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get tag with repo name: {}, result: {}'.format(repo_name, result))
        else:
            logging.error('Failed to get tags with repo name: {}'.format(repo_name))
        return result

    # GET /repositories/manifests
    def get_repository_manifests(self, repo_name, tag):
        result = None
        path = '{}://{}/api/repositories/manifests?repo_name={}&tag={}'.format(self.protocol, self.host, repo_name, tag)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get manifests with repo name: {}, tag: {}, result: {}'.format(repo_name,
                                                                                                      tag, result))
        else:
            logging.error('Failed to get manifests with repo name: {}, tag: {}'.format(repo_name, tag))
        return result

    # GET /repositories/top
    def get_top_accessed_repositories(self, count=None):
        result = None
        path = '{}://{}/api/repositories/top'.format(self.protocol, self.host)
        if count:
            path += "?count={}".format(count)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get top accessed repositories, result: {}'.format(result))
        else:
            logging.error('Failed to get top accessed repositories')
        return result

    # GET /logs
    def get_logs(self, lines=None, start_time=None, end_time=None):
        result = None
        path = '{}://{}/api/logs'.format(self.protocol, self.host)
        response = requests.get(path, cookies={'beegosessionID': self.session_id})

        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get logs')
        else:
            logging.error('Failed to get logs and response code: {}'.format(response.status_code))
        return result

    def get_system_info(self):
        """
        GET /systeminfo
        Get general system info
        :return: JSON with system info
        """
        endpoint = '/api/systeminfo'
        path = '{}/{}'.format(self.based_url, endpoint)
        response = requests.get(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get system info: {}'.format(result))
            return result
        else:
            logging.error('Failed to get system info')

    def get_system_info_volumes(self):
        """
        GET /systeminfo/volumes
        Get system volume info (total/free size).
        :return: JSON with system info volumes
        """
        endpoint = '/api/systeminfo/volumes'
        path = '{}/{}'.format(self.based_url, endpoint)
        response = requests.get(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = response.json()
            logging.debug('Successfully get system info: {}'.format(result))
            return result
        elif response.status_code == 401:
            logging.info('Need to be logged in.')
        elif response.status_code == 403:
            logging.info('User does not have permission of admin role.')
        else:
            logging.error('Failed to get system info volumes')

    def get_configurations(self):
        """
        GET /configurations
        Get system configurations
        :return: JSON with configurations
        """
        endpoint = '/api/configurations'
        path = '{}/{}'.format(self.based_url, endpoint)
        response = requests.get(path, cookies={'beegosessionID': self.session_id}, verify=self.verify_ssl_cert)
        if response.status_code == 200:
            result = response.json()
            logging.debug('Get system configurations successfully: {}'.format(result))
            return result
        elif response.status_code == 401:
            logging.info('Need to be logged in.')
        elif response.status_code == 403:
            logging.info('User does not have permission of admin role.')
        else:
            logging.error('Failed to get configurations')


# TODO: remove it
"""
this part only for testing
./harborclient.py --user admin --host harbor.lss.emc.com --passwd VERY_SECRET_PASSWORD
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-a', dest='host', help='harbor address', required=True)
    parser.add_argument('--user', '-u', dest='user', help='user name', required=True)
    parser.add_argument('--passwd', '-p', dest='passwd', help='password', required=True)
    parsed_args = parser.parse_args()

    logging.info(parsed_args)

    client = HarborClient(host=parsed_args.host,
                          user=parsed_args.user,
                          password=parsed_args.passwd,
                          protocol='https',
                          verify_ssl_cert=False)

