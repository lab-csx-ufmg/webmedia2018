import os
import unittest

from GitHubAPI import GitHubUser
from fields import FIELDS_USER, FIELDS_ORGANIZATION, FIELDS_REPO

USERNAME = 'gaearon'


class GitHubUserTest(unittest.TestCase):
    def setUp(self):
        git_user = None
        git_token = None
        if os.environ.get('GIT_USER'):
            git_user = os.environ.get('GIT_USER')
        if os.environ.get('GIT_TOKEN'):
            git_token = os.environ.get('GIT_TOKEN')

        self.user = GitHubUser(USERNAME, git_user=git_user, git_token=git_token)
        pass

    def tearDown(self):
        pass

    def test_info(self):
        assert self.user.info
        for key in FIELDS_USER:
            assert key in self.user.info

    def test_followers(self):
        assert self.user.followers
        assert len(self.user.followers) > 0

        assert self.user.followers[0]
        for key in FIELDS_USER:
            assert key in self.user.followers[0].info

    def test_following(self):
        assert self.user.following
        assert len(self.user.following) > 0

        assert self.user.following[0]
        for key in FIELDS_USER:
            assert key in self.user.following[0].info

    def test_repos(self):
        assert self.user.repos
        assert len(self.user.repos) > 0

        assert self.user.repos[0]
        for key in FIELDS_REPO:
            assert key in self.user.repos[0].info

    def test_organizations(self):
        assert self.user.organizations
        assert len(self.user.organizations) > 0

        assert self.user.organizations[0]
        for key in FIELDS_ORGANIZATION:
            assert key in self.user.organizations[0].info
