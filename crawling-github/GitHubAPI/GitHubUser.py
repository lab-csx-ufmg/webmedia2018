import GitHubAPI

class GitHubUser(GitHubAPI.GitHubBase):
    USER_URL = "{baseUrl}/users/{username}"
    def __init__(
        self,
        username,
        info=None,
        followers=None,
        following=None,
        organizations=None,
        repos=None,
        git_user=None,
        git_token=None
    ):
        super().__init__(git_user, git_token)

        self.__username = username
        self.__info = info
        self.__followers = followers
        self.__following = following
        self.__organizations = organizations
        self.__repos = repos

    def __str__(self):
        return "GitHubUser(name={username})".format(username=self.username)

    @property
    def username(self):
        return self.__username

    @property
    def info(self):
        if self.__info:
            return self.__info
        else:
            self.__info = self.request_api(
                GitHubAPI.GitHubUser.USER_URL.format(
                    baseUrl=GitHubAPI.GitHubBase.BASE_URL,
                    username=self.username
                )
            )
            return self.__info

    @property
    def followers(self):
        if self.__followers:
            return self.__followers
        else:
            self.__followers = [
                GitHubAPI.GitHubUser(username=info['login'], info=info)
                for info in self.request_api(self.info['followers_url'])
            ]

            return self.__followers

    @property
    def following(self):
        if self.__following:
            return self.__following
        else:
            self.__following = [
                GitHubUser(username=info['login'], info=info)
                for info in self.request_api(self.info['following_url'].replace('{/other_user}', ''))
            ]
            return self.__following

    @property
    def organizations(self):
        if self.__organizations:
            return self.__organizations
        else:
            print(self.info)
            self.__organizations = [
                GitHubAPI.GitHubOrganization(name=info['login'], info=info)
                for info in self.request_api(self.info['organizations_url'])
            ]
            return self.__organizations

# class GitHubAPI(GitHubBase):
#     def request_api(self, url,data={}):
#         headers = {'User-Agent': GIT_USER_NAME}
#         if AUTH_TOKEN :
#             headers["Authorization"] = 'token ' + AUTH_TOKEN
#
#         r = requests.get(url, headers=headers)
#         return json.loads(r.text or r.content)
#
#     def get_repo_from_user(self, username):
#         return self.request_api(BASE_URL+"/users/"+username+"/repos")
#
#     def user_following(self, username):
#         return self.request_api(USERS_URL.format(url=BASE_URL, username=username, endpoint="following"))
#
#     def get_user_followers(self, username):
#         return self.request_api(USERS_URL.format(url=BASE_URL, username=username, endpoint="followers"))
#
#     def get_contributors_from_repo(self, userOwner,repoName):
#         '''
#         Contributor: A contributor is someone from the outside not on the core development team of the project that wants to contribute some changes to a project.
#         https://github.com/CoolProp/CoolProp/wiki/Contributors-vs-Collaborators
#         '''
#         return self.request_api(BASE_URL+"/repos/"+userOwner+"/"+repoName+"/contributors")
#
#     def get_collaborators_from_repo(self, userOwner,repoName):
#         '''
#         Requires authentication
#         Collaborator: A collaborator is someone on the core development team of the project and has commit access to the main repository of the project.
#         https://github.com/CoolProp/CoolProp/wiki/Contributors-vs-Collaborators
#         '''
#         return self.request_api(BASE_URL+"/repos/"+userOwner+"/"+repoName+"/collaborators")
