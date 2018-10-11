import requests
import json

GIT_USER_NAME = "daniel-hasan"
URL_BASE = "https://api.github.com"
def request_github_api(url,data={}):
    headers = {'User-Agent': GIT_USER_NAME}

    r= requests.get(url, headers=headers)
    return json.loads(r.text or r.content)

def get_repo_from_user(userName):
    return request_github_api(URL_BASE+"/users/"+userName+"/repos")

def get_contributors_from_repo(userOwner,repoName):
    return request_github_api(URL_BASE+"/repos/"+userOwner+"/"+repoName+"/contributors")




if __name__ == "__main__":
  print(get_contributors_from_repo("daniel-hasan","cefet-web-coral55"))
