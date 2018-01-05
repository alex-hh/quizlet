import requests
import json
import urllib
import random
import string
import base64

#author: Tobias Domhan
# https://github.com/tdomhan/pyquizlet


class Quizlet():
    def __init__(self, qid):
        self.qid = qid
        self.base_url = "https://api.quizlet.com/2.0/"
        self.authorized = False
        self.access_token = None

    #generate an authentication url 
    #redirect the user to this url
    def generate_auth_url(self, scopes):
        #TODO: check if scope is a list of strings
        #TODO: url redirect parameter
        auth_url = 'https://quizlet.com/authorize/'
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
        params = {'scope': " ".join(scopes),
                  'client_id': self.qid,
                  'response_type': 'code',
                  'state': state }
        request_string = auth_url + '?' + urllib.urlencode(params)

        return (request_string,state)

    def request_token(self, code, redirect_uri, secret):
        self.authorized = False
        auth_url = 'https://api.quizlet.com/oauth/token'
        params = {'grant_type': 'authorization_code',
                  'code': code,
                  'redirect_uri': redirect_uri}
        auth = base64.encodestring(('%s:%s' % (self.qid, secret)).encode()).decode().replace('\n', '')
        #auth = base64.encodestring( self.qid + ':' + secret)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Authorization' : 'Basic ' + auth}

        #h.add_credentials(self.qid, secret)

        response = requests.post(auth_url, headers=headers, data=params)

        if response.status_code != '200':
            raise Exception("request not successful(return code: %s): %s" % (response.status_code, response.content))

        response_data = response.json()
        self.access_token = response_data
        print(response_data)
        self.authorized = True

