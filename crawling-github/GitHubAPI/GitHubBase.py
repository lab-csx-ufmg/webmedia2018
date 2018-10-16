import os
import requests
import json

from GitHubAPI.credentials import GIT_USER, GIT_TOKEN

'''
GitHubBase: class that is base for github requests
'''
class GitHubBase():
    BASE_URL = "https://api.github.com"

    def __init__(self, user=None, token=None):
        self.user = user or ('GIT_USER' in os.environ and os.environ['GIT_USER']) or GIT_USER
        self.token = token or ('GIT_TOKEN' in os.environ and os.environ['GIT_TOKEN']) or GIT_TOKEN

    def request_api(self, url, data={}):
        headers = {}
        if self.user:
            headers = {'User-Agent': self.user}
        if self.token:
            headers["Authorization"] = "token {token}".format(token=self.token)

        r = requests.get(url, headers=headers)
        if 'application/json' in r.headers.get('content-type'):
            return json.loads(r.text or r.content)
        return {}
