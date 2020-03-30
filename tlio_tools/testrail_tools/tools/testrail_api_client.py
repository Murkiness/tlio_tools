import requests
import json
import base64
import argparse
import time
import os

user = os.environ["TESTRAIL_EMAIL"]
password = os.environ["TESTRAIL_KEY"]

class APIClient:
    def __init__(self, base_url):
        self.user = user
        self.password = password
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    def send_get(self, uri, filepath=None):
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code != 200:
                    print(f"Result was not posted for url: {uri}")
                    print(response.status_code)
                    print(response.json())
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except: # Nothing to return
                    return {}


    def update_result_on_testrail(self, status, test_id):
        return self.send_post(f"add_result/{test_id}", {"status_id": status})

    def get_sections(self, project_id, suite_id):
        return self.send_get(f"get_sections/{project_id}&suite_id={suite_id}")

    def get_cases(self, project_id, suite_id, section_id=None):
        if section_id is None:
            return self.send_get(f"get_cases/{project_id}&suite_id={suite_id}")
        return self.send_get(f"get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}")

    def update_case(self, case_id, **kwargs):
        return self.send_post(f"update_case/{case_id}", kwargs)

    def get_case(self, case_id):
        return self.send_get(f"get_case/{case_id}")

    def get_plans(self, project_id, milestone_id):
        return self.send_get(f"/get_plans/{project_id}&milestone_id={milestone_id}")

    def get_plan(self, plan_id):
        return self.send_get(f"/get_plan/{plan_id}")

    def get_tests(self, run_id):
        return self.send_get(f"/get_tests/{run_id}")

    def get_sections(self, project_id, suite_id):
        return self.send_get(f"/get_sections/{project_id}&suite_id={suite_id}")

    def get_suites(self, project_id):
        return self.send_get(f"/get_suites/{project_id}")  

    def get_all_cases(self):
        # helper method with hardcoded values
        PROJECT_ID = 12
        SUITE_ID = 23

        return self.get_cases(PROJECT_ID, SUITE_ID)


class APIError(Exception):
    pass
