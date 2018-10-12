import unittest

from GitHubAPI import GitHubOrganization
from fields import FIELDS_USER, FIELDS_ORGANIZATION, FIELDS_REPO

ORGANIZATION_NAME = 'facebook'


class GitHubOrganizationTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_info(self):
        org = GitHubOrganization(ORGANIZATION_NAME)

        assert org.info
        for key in FIELDS_ORGANIZATION:
            assert key in org.info

    def test_public_members(self):
        api = GitHubOrganization(ORGANIZATION_NAME)

        assert api.public_members
        assert len(api.public_members) > 0

        assert api.public_members[0]
        for key in FIELDS_USER:
            assert key in api.public_members[0].info

    def test_repos(self):
        api = GitHubOrganization(ORGANIZATION_NAME)

        assert api.repos
        assert len(api.repos) > 0

        assert api.repos[0]
        for key in FIELDS_REPO:
            assert key in api.repos[0].info
