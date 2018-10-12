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

    @property
    def repos(self):
        if self.__repos:
            return self.__repos
        else:
            self.__repos = [
                GitHubAPI.GitHubRepo(owner=info['owner'], name=info['name'], info=info)
                for info in self.request_api(self.info['repos_url'])
            ]

            return self.__repos
