import GitHubAPI

class GitHubRepo(GitHubAPI.GitHubBase):
    REPO_URL = "{baseUrl}/repos/{owner}/{repo}"
    def __init__(
        self,
        owner,
        name,
        info=None,
        contributors=None,
        git_user=None,
        git_token=None
    ):
        super().__init__(git_user, git_token)

        if type(owner) is GitHubAPI.GitHubUser:
            self.__owner = owner
        elif type(owner) is dict:
            self.__owner = GitHubAPI.GitHubUser(username=owner['login'], info=owner)
        else:
            self.__owner = GitHubAPI.GitHubUser(username=owner, info=owner)

        self.__name = name
        self.__info = info
        self.__contributors = contributors

    def __str__(self):
        return "GitHubRepo(name={full_name})".format(full_name=self.info['full_name'])

    @property
    def owner(self):
        return self.__owner

    @property
    def name(self):
        return self.__name

    @property
    def info(self):
        if self.__info:
            return self.__info
        else:
            self.__info = self.request_api(
                GitHubRepo.REPO_URL.format(
                    baseUrl=GitHubAPI.GitHubBase.BASE_URL,
                    owner=self.owner.username,
                    repo=self.name,
                )
            )
            return self.__info

    @property
    def contributors(self):
        if self.__contributors:
            return self.__contributors
        else:
            self.__contributors = [
                GitHubAPI.GitHubUser(cont['login'], cont)
                for cont in self.request_api(self.info['contributors_url'])
            ]

            return self.__contributors
