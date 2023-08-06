#
# Python 3.*
# pip install requests
#

import requests
# import json
# from pprint import pprint


class Friendlyscore:

    def __init__(self, cid, sec):
        self.by = None
        self.id = None
        self.client_id = cid
        self.client_secret = sec
        self.base_url = 'https://friendlyscore.com/'
        self.request_token_url = self.base_url + 'oauth/v2/token'

    def setBaseUrl(self, url):
        self.base_url = url.rstrip('/') + '/'
        self.request_token_url = self.base_url + 'oauth/v2/token'

    def getToken(self):
        credentials = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
                }

        r = requests.post(self.request_token_url, json=credentials)
        token = r.json()

        # TODO
        # if token['error'] == 'invalid_client' → exception

        self.auth_headers = {'Authorization': 'Bearer '+token['access_token']}
        return r.status_code, token

    def url(self, endpoint):
        return self.base_url+'api/v2/'+endpoint+'.json'

    def get(self, endpoint, params={}):
        r = requests.get(self.url(endpoint), params=params,
                         headers=self.auth_headers)
        if r.status_code == 204:
            return 204, None
        return r.status_code, r.json()

    def post(self, endpoint, params={}):
        r = requests.post(self.url(endpoint), json=params,
                          headers=self.auth_headers)
        if r.status_code == 204:
            return 204, None
        return r.status_code, r.json()

    def put(self, endpoint, params={}):
        r = requests.put(self.url(endpoint), json=params,
                         headers=self.auth_headers)
        if r.status_code == 204:
            return 204, None
        return r.status_code, r.json()

    def users(self, page=1, max_results=20):
        self.getToken()
        return self.get('users', {
            'page': page,
            'max_results': max_results
            })

    def by_id(self, id):
        self.by = 'id'
        self.id = id
        return self

    def by_partner_id(self, id):
        self.by = 'partner-id'
        self.id = id
        return self

    def calculate_score(self, params):
        self.getToken()
        return self.post("users/{0}/{1}/calculate_score"
                         .format(self.by, self.id), params)

    def user(self):
        self.getToken()
        return self.get("users/{0}/{1}/show"
                        .format(self.by, self.id))

    def google_places_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/places"
                        .format(self.by, self.id))

    def google_dob_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/days-of-birth"
                        .format(self.by, self.id))

    def google_skills_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/skills"
                        .format(self.by, self.id))

    def google_phones_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/phones"
                        .format(self.by, self.id))

    def google_work_periods_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/work-periods"
                        .format(self.by, self.id))

    def google_universities_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/universities"
                        .format(self.by, self.id))

    def google_emails_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google/raw-file-data/emails"
                        .format(self.by, self.id))

    def user_ip_address_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/show/ip-address-data"
                        .format(self.by, self.id))

    def user_min_fraud_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/show/min-fraud-data"
                        .format(self.by, self.id))

    def add_user_performance_data(self, params):
        self.getToken()
        return self.post("users/{0}/{1}/performance-data"
                         .format(self.by, self.id), params)

    def set_positive(self, val):
        self.getToken()
        return self.put("users/{0}/{1}/positive/{2}"
                        .format(self.by, self.id, '1' if val else '0'))

    def set_status(self, status, description):
        params = {
            'status':      status,
            'description': description
        }
        self.getToken()
        return self.post("users/{0}/{1}/status"
                         .format(self.by, self.id), params)

