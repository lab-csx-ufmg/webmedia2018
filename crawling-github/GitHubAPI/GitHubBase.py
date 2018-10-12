import requests
import json

'''
GitHubBase: class that is base for github requests
'''
class GitHubBase():
    BASE_URL = "https://api.github.com"

    def __init__(self, user=None, token=None):
        self.user = user
        self.token = token

    def request_api(self, url, data={}):
        headers = {}
        if self.user:
            headers = {'User-Agent': self.user}
        if self.token:
            headers["Authorization"] = "token {token}".format(token=self.token)

        r = requests.get(url, headers=headers)
        return json.loads(r.text or r.content)
