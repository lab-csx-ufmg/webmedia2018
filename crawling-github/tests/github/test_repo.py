import unittest

from GitHubAPI import GitHubRepo
from fields import FIELDS_USER, FIELDS_ORGANIZATION, FIELDS_REPO

OWNER_NAME = 'gaearon'
REPO_NAME = 'disposables'

class GitHubRepoTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_info(self):
        org = GitHubRepo(OWNER_NAME, REPO_NAME)

        assert org.info
        for key in FIELDS_REPO:
            assert key in org.info

    def test_contributors(self):
        api = GitHubRepo(OWNER_NAME, REPO_NAME)

        assert api.contributors
        assert len(api.contributors) > 0

        assert api.contributors[0]
        for key in FIELDS_USER:
            assert key in api.contributors[0].info
