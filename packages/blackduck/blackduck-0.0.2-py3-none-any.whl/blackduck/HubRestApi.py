'''
Created on Jul 6, 2018

@author: kumykov

Wrapper for common HUB API queries. 
Upon initialization Bearer tocken is obtained and used for all subsequent calls

Usage: 

credentials and hub URL could be placed in the .restconfig.json file
    
    {
      "baseurl": "https://hub-hostname",
      "username": "<username goes here>",
      "password": "<password goes here>",
      "insecure": true,
      "debug": false
    }

    OR, using API Token

    {
      "baseurl": "https://hub-hostname",
      "api_token": "<API token goes here>",
      "insecure": true,
      "debug": false
    }

    .restconfig.json should be present in the current directory.
    
    from blackduck.HubRestApi import HubInstance
    
    hub = HubInstance()
    projects = hub.get_projects()

It is possible to generate generate_config file by initalizing API as following:
   
    from blackduck.HubRestApi import HubInstance
    
    username="<username goes here>"
    password="<password goes here>"
    urlbase="https://hub-hostname"
    
    hub = HubInstance(urlbase, username, password, insecure=True)
    
    
'''
import logging
import requests
import json

class CreateFailedAlreadyExists(Exception):
    pass

class CreateFailedUnknown(Exception):
    pass

class HubInstance(object):
    '''
    classdocs
    '''
    # TODO: What to do about the config file for thread-safety, concurrency
    configfile = ".restconfig.json"

    def __init__(self, *args, **kwargs):
        # Config needs to be an instance variable for thread-safety, concurrent use of HubInstance()
        self.config = {}

        try:
            self.config['baseurl'] = args[0]
            api_token = kwargs.get('api_token', False)
            if api_token:
                self.config['api_token'] = api_token
            else:
                self.config['username'] = args[1]
                self.config['password'] = args[2]
            self.config['insecure'] = kwargs.get('insecure', False)
            self.config['debug'] = kwargs.get('insecure', False)

            if kwargs.get('write_config_flag', True):
                self.write_config()
        except Exception:
            self.read_config()
            
        if self.config['insecure']:
            requests.packages.urllib3.disable_warnings()
        
        if self.config['debug']:
            print(self.configfile)
        
        self.token, self.csrf_token = self.get_auth_token()
        
        
    def read_config(self):
        with open('.restconfig.json','r') as f:
            self.config = json.load(f)
            
    def write_config(self):
        with open(self.configfile,'w') as f:
            json.dump(self.config, f, indent=3)
          
    def get_auth_token(self):
        api_token = self.config.get('api_token', False)
        if api_token:
            authendpoint = "/api/tokens/authenticate"
            url = self.config['baseurl'] + authendpoint
            session = requests.session()
            response = session.post(
                url, 
                data={}, 
                headers={'Authorization': 'token {}'.format(api_token)}, 
                verify=not self.config['insecure']
            )
            csrf_token = response.headers['X-CSRF-TOKEN']
            bearer_token = json.loads(response.content.decode('utf-8'))['bearerToken']
            return (bearer_token, csrf_token)
        else:
            authendpoint="/j_spring_security_check"
            url = self.config['baseurl'] + authendpoint
            session=requests.session()
            credentials = dict()
            credentials['j_username'] = self.config['username']
            credentials['j_password'] = self.config['password']
            response = session.post(url, credentials, verify= not self.config['insecure'])
            cookie = response.headers['Set-Cookie']
            token = cookie[cookie.index('=')+1:cookie.index(';')]
        return (token, None)
    
    def get_urlbase(self):
        return self.config['baseurl']

    def get_headers(self):
        if self.config.get('api_token', False):
            return {
                'X-CSRF-TOKEN': self.csrf_token, 
                'Authorization': 'Bearer {}'.format(self.token), 
                'Content-Type': 'application/json'}
        else:
            return {"Authorization":"Bearer " + self.token}

    def get_api_version(self):
        url = self.get_urlbase() + '/api/current-version'
        response = self.execute_get(url)
        version = response.json().get('version', 'unknown')
        return version

    def _get_parameter_string(self, parameters={}):
        parameter_string = "&".join(["{}={}".format(k,v) for k,v in parameters.items()])
        return "?" + parameter_string

    def _get_policy_url(self):
        return self.config['baseurl'] + "/api/policy-rules"

    def get_policies(self, parameters={}):
        url = self._get_policy_url() + self._get_parameter_string(parameters)
        response = self.execute_get(url)
        return response.json()

    def create_policy(self, policy_json):
        url = self._get_policy_url()
        location = self._create(url, policy_json)
        return location

    def get_policy_by_id(self, policy_id):
        url = self._get_policy_url() + "/{}".format(policy_id)
        return self.get_policy_by_url(url)

    def get_policy_by_url(self, policy_url):
        response = self.execute_get(policy_url)
        jsondata = response.json()
        return jsondata

    def update_policy_by_id(self, policy_id, update_json):
        url = self._get_policy_url() + "/{}".format(policy_id)
        return self.update_policy_by_url(url, update_json)

    def update_policy_by_url(self, policy_url, update_json):
        return self.execute_put(policy_url, update_json)

    def delete_policy_by_id(self, policy_id):
        url = self._get_policy_url() + "/{}".format(policy_id)
        return self.delete_policy_by_url(url)

    def delete_policy_by_url(self, policy_url):
        return self.execute_delete(policy_url)

    def find_component_info_for_protex_component(self, protex_component_id, protex_component_release_id):
        '''Will return the Hub component corresponding to the protex_component_id, and if a release (version) id
        is given, the response will also include the component-version. Returns an empty list if there were
        no components found.
        '''
        url = self.config['baseurl'] + "/api/components"
        if protex_component_release_id:
            query = "?q=bdsuite:{}%23{}&limit=9999".format(protex_component_id, protex_component_release_id)
        else:
            query = "?q=bdsuite:{}&limit=9999".format(protex_component_id)
        with_query = url + query
        logging.debug("Finding the Hub componet for Protex component id {}, release id {} using query/url {}".format(
            protex_component_id, protex_component_release_id, with_query))
        response = self.execute_get(with_query)
        logging.debug("query results in status code {}, json data: {}".format(response.status_code, response.json()))
        # TODO: Error checking and retry? For now, as POC just assuming it worked
        component_list_d = response.json()
        if component_list_d['totalCount'] >= 1:
            return component_list_d['items'][0]
        else:
            return component_list_d['items']

    def get_limit_paramstring(self, limit):
        return "?limit={}".format(limit)

    def get_apibase(self):
        return self.config['baseurl'] + "/api"
    
    def get_projects(self, limit=100):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.config['baseurl'] + "/api/projects" + paramstring
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_project_by_id(self, project_id, limit=100):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.config['baseurl'] + "/api/projects/" + project_id + paramstring
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_project_versions(self, project, limit=100):
        paramstring = self.get_limit_paramstring(limit)
        url = project['_meta']['href'] + "/versions" + paramstring
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_version_by_id(self, project_id, version_id, limit=100):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.config['baseurl'] + "/api/projects/" + project_id + "/versions/" + version_id
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
        
    def get_version_components(self, projectversion, limit=1000):
        paramstring = self.get_limit_paramstring(limit)
        url = projectversion['_meta']['href'] + "/components" + paramstring
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_file_matches_for_component_no_version(self, project_id, version_id, component_id, limit=1000):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.get_apibase() + \
            "/projects/{}/versions/{}/components/{}/matched-files".format(project_id, version_id, component_id)
        print("GET ", url)
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_file_bom_entries(self, hub_release_id, limit=100):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.get_apibase() + \
            "/v1/releases/{}/file-bom-entries".format(hub_release_id)
        print("GET ", url)
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata


    def get_file_matches_for_component_with_version(self, project_id, version_id, component_id, component_version_id, limit=1000):
        headers = self.get_headers()
        paramstring = self.get_limit_paramstring(limit)
        url = self.get_apibase() + \
            "/projects/{}/versions/{}/components/{}/versions/{}/matched-files".format(project_id, version_id, \
                component_id, component_version_id)
        print("GET ", url)
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata


    def get_snippet_bom_entries(self, project_id, version_id, reviewed=False, included=False, limit=100, offset=0):
        headers = self.get_headers()
        paramstring = "?limit=" + str(limit) + "&offset=" + \
            str(offset) + "&filter=bomReviewStatus:" + str(reviewed).lower() + "&filter=bomInclusion:" + str(included).lower()
        path = self.get_apibase() + \
            "/internal/projects/{}/versions/{}/snippet-bom-entries".format(project_id, version_id)
        url = path + paramstring
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def ignore_snippet_bom_entry(self, hub_version_id, snippet_bom_entry):
        headers = self.get_headers()
        headers['ContentType'] = "application/json"
        url = self.get_apibase() + \
            "/v1/releases/{}/snippet-bom-entries".format(hub_version_id)
        body = self.get_ignore_snippet_json(snippet_bom_entry)
        response = requests.put(url, json=body, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
        return 0

    def get_ignore_snippet_json(self, snippet_bom_entry):
        for cur_fileSnippetBomComponents in snippet_bom_entry['fileSnippetBomComponents']:
            cur_fileSnippetBomComponents['ignored'] = True
        return [snippet_bom_entry]
    
    def compare_project_versions(self, version, compareTo):
        apibase = self.config['baseurl'] + "/api"
        paramstring = "?limit=1000&sortField=component.securityRiskProfile&ascending=false&offset=0"
        cwhat = version['_meta']['href'].replace(apibase, '')
        cto = compareTo['_meta']['href'].replace(apibase, '')
        url = apibase + cwhat + "/compare" + cto + "/components" + paramstring
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
    
    def get_version_codelocations(self, version, limit=100):
        apibase = self.config['baseurl'] + "/api"
        paramstring = "?limit=100&offset=0"
        projectversion = version['_meta']['href']
        url = projectversion + "/codelocations" + paramstring
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
        
    def get_codelocations(self, limit=100):
        paramstring = "?limit={}&offset=0".format(limit)
        headers = self.get_headers()
        url = self.get_apibase() + "/codelocations" + paramstring
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def get_codelocation_scan_summaries(self, code_location_id, limit=100):
        paramstring = "?limit={}&offset=0".format(limit)
        headers = self.get_headers()
        url = self.get_apibase() + \
            "/codelocations/{}/scan-summaries".format(code_location_id)
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
    
    def get_component_by_id(self, component_id):
        url = self.config['baseurl'] + "/api/components/{}".format(component_id)
        return self.get_component_by_url(url)

    def get_component_by_url(self, component_url):
        response = self.execute_get(component_url)
        jsondata = response.json()
        return jsondata

    def get_scanlocations(self):
        url = self.config['baseurl'] + "/api/v1/scanlocations"
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def update_component_by_id(self, component_id, update_json):
        url = self.config["baseurl"] + "/api/components/{}".format(component_id)
        return self.update_component_by_url(url, update_json)

    def update_component_by_url(self, component_url, update_json):
        return self.execute_put(component_url, update_json)

    def delete_codelocation(self, locationid):
        url = self.config['baseurl'] + "/api/codelocations/" + locationid
        headers = self.get_headers()
        response = requests.delete(url, headers=headers, verify = not self.config['insecure'])
        return response

    def execute_delete(self, url):
        headers = self.get_headers()
        response = requests.delete(url, headers=headers, verify = not self.config['insecure'])
        return response

    def get_ldap_state(self):
        url = self.config['baseurl'] + "/api/v1/ldap/state"
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata

    def enable_ldap(self):
        url = self.config['baseurl'] + "/api/v1/ldap/state"
        headers = self.get_headers()
        payload = {}
        payload['ldapEnabled'] = True
        response = requests.post(url, headers=headers, verify = not self.config['insecure'], json=payload)
        jsondata = response.json()
        return jsondata
        
    def disable_ldap(self):
        url = self.config['baseurl'] + "/api/v1/ldap/state"
        headers = self.get_headers()
        payload = {}
        payload['ldapEnabled'] = False
        response = requests.post(url, headers=headers, verify = not self.config['insecure'], json=payload)
        jsondata = response.json()
        return jsondata
        
    def get_ldap_configs(self):
        url = self.config['baseurl'] + "/api/v1/ldap/configs"
        headers = self.get_headers()
        headers['Content-Type']  = "application/json"
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        jsondata = response.json()
        return jsondata
    
    def _validated_json_data(self, data_to_validate):
        if isinstance(data_to_validate, dict):
            json_data = json.dumps(data_to_validate)
        else:
            json_data = data_to_validate
        return json_data

    def execute_get(self, url):
        headers = self.get_headers()
        response = requests.get(url, headers=headers, verify = not self.config['insecure'])
        return response
        
    def execute_put(self, url, data):
        data = self._validated_json_data(data)
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.put(url, headers=headers, data=data, verify = not self.config['insecure'])
        return response

    def _create(self, url, json_body):
        response = self.execute_post(url, json_body)
        if response.status_code == 201 and "location" in response.headers:
            return (response.headers["location"])
        elif response.status_code == 412:
            raise CreateFailedAlreadyExists("Failed to create the object because it already exists - url {}, body {}, response {}".format(url, json_body, response))
        else:
            raise CreateFailedUnknown("Failed to create the object for an unknown reason - url {}, body {}, response {}".format(url, json_body, response))

    def execute_post(self, url, data):
        data = self._validated_json_data(data)
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, data=data, verify = not self.config['insecure'])
        return response


