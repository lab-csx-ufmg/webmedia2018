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
    '''
    Contributor: A contributor is someone from the outside not on the core development team of the project that wants to contribute some changes to a project.
    https://github.com/CoolProp/CoolProp/wiki/Contributors-vs-Collaborators
    '''
    return request_github_api(URL_BASE+"/repos/"+userOwner+"/"+repoName+"/contributors")

def get_collaborators_from_repo(userOwner,repoName):
    '''
    Requires authentication
    Collaborator: A collaborator is someone on the core development team of the project and has commit access to the main repository of the project.
    https://github.com/CoolProp/CoolProp/wiki/Contributors-vs-Collaborators
    '''
    return request_github_api(URL_BASE+"/repos/"+userOwner+"/"+repoName+"/collaborators")





if __name__ == "__main__":
  print(get_collaborators_from_repo("daniel-hasan","cefet-web"))
