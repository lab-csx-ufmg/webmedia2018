import os
import unittest

from GitHubAPI import GitHubRepo
from fields import FIELDS_USER, FIELDS_ORGANIZATION, FIELDS_REPO

OWNER_NAME = 'gaearon'
REPO_NAME = 'disposables'

class GitHubRepoTest(unittest.TestCase):
    def setUp(self):
        git_user = None
        git_token = None
        if os.environ.get('GIT_USER'):
            git_user = os.environ.get('GIT_USER')
        if os.environ.get('GIT_TOKEN'):
            git_token = os.environ.get('GIT_TOKEN')

        self.repo = GitHubRepo(OWNER_NAME, REPO_NAME, git_user=git_user, git_token=git_token)
        pass

    def tearDown(self):
        pass

    def test_info(self):
        assert self.repo.info
        for key in FIELDS_REPO:
            assert key in self.repo.info

    def test_contributors(self):
        assert self.repo.contributors
        assert len(self.repo.contributors) > 0

        assert self.repo.contributors[0]
        for key in FIELDS_USER:
            assert key in self.repo.contributors[0].info
