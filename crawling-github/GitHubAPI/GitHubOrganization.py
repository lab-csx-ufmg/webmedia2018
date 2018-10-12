import GitHubAPI

class GitHubOrganization(GitHubAPI.GitHubBase):
    ORGANIZATION_URL = "{baseUrl}/orgs/{org}"
    def __init__(
        self,
        name,
        info=None,
        repos=None,
        events=None,
        public_members=None,
        git_user=None,
        git_token=None
    ):
        super().__init__(git_user, git_token)

        self.__name = name
        self.__info = info
        self.__repos = repos
        self.__public_members = public_members

    def __str__(self):
        return "GitHubOrganization(name={name})".format(name=self.name)

    @property
    def name(self):
        return self.__name

    @property
    def info(self):
        if self.__info:
            return self.__info
        else:
            self.__info = self.request_api(
                GitHubOrganization.ORGANIZATION_URL.format(
                    baseUrl=GitHubAPI.GitHubBase.BASE_URL,
                    org=self.name
                )
            )
            return self.__info

    @property
    def public_members(self):
        if self.__public_members:
            return self.__public_members
        else:
            self.__public_members = [
                GitHubAPI.GitHubUser(username=info['login'], info=info)
                for info in self.request_api(self.info['public_members_url'].replace('{/member}', ''))
            ]

            return self.__public_members

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
