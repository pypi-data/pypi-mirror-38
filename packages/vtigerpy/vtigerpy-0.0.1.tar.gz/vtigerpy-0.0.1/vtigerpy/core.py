import requests
import hashlib
import json


class Vtiger(object):

    def __init__(self, endpoint, username, accessKey, sessionName=None):
        self.endpoint = endpoint
        self.username = username
        self.accessKey = accessKey
        self.sessionName = sessionName

        if self.sessionName is None:
            self.auth()

    def auth(self, **kwargs):
        url_challenge = '/webservice.php?operation=getchallenge&username={}'.format(
            self.username)
        url_session = '/webservice.php'

        r = requests.post(self.endpoint+url_challenge)
        if (r.status_code == 200) and ('success' in r.json()):
            if r.json()['success']:
                k = r.json()['result']['token']
                payload = {'operation': 'login',
                           'username': self.username,
                           'accessKey': hashlib.md5((k+self.accessKey).encode()).hexdigest()}

                rr = requests.post(self.endpoint+url_session, data=payload)

                if rr.status_code == 200 and ('success' in rr.json()):
                    if rr.json()['success']:
                        self.sessionName = rr.json()['result']['sessionName']
                    else:
                        raise Exception(rr.json())
                else:
                    raise Exception(rr.json())
            else:
                raise Exception(r.json())
        else:
            raise Exception(r.json())

    def set_formparams(self, operation=None, **kwargs):
        v = {**{'operation': operation, 'sessionName': self.sessionName}, **kwargs}
        if v['operation'] is None:
            v.pop('operation')
        return v

    def post(self, operation=None, url='/webservice.php', **kwargs):
        r = requests.post(self.endpoint+url,
                          self.set_formparams(operation, **kwargs))
        return r

    def get(self, operation=None, url='/webservice.php', **kwargs):
        r = requests.get(self.endpoint+url,
                         params=self.set_formparams(operation, **kwargs))
        return r
