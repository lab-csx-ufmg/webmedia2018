import requests
import json


URL_BASE = "https://api.github.com"
#To authenticate: https://github.com/settings/developers
GIT_USER_NAME = "usuario-git"
AUTH_TOKEN = "5b1dbfa50f221f3486f27ae2d6f017d8d8a5b910"
def request_github_api(url,data={}):
    headers = {'User-Agent': GIT_USER_NAME,#It is adviced to put the user name as the user-agent
                "Accept": "application/vnd.github.v3+json"}
    if AUTH_TOKEN:
        headers["Authorization"] = 'token ' + AUTH_TOKEN

    r= requests.get(url, headers=headers, data=data)
    return json.loads(r.text or r.content)

def get_repo_from_user(userName):
    return request_github_api(URL_BASE+"/users/"+userName+"/repos")

def get_user_following(userName):
    return request_github_api(URL_BASE+"/users/"+userName+"/following")

def get_user_followers(userName):
    return request_github_api(URL_BASE+"/users/"+userName+"/followers")

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
