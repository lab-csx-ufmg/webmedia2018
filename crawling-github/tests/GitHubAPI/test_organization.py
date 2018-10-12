import os
import unittest

from GitHubAPI import GitHubOrganization
from fields import FIELDS_USER, FIELDS_ORGANIZATION, FIELDS_REPO

ORGANIZATION_NAME = 'facebook'


class GitHubOrganizationTest(unittest.TestCase):
    def setUp(self):
        self.org = GitHubOrganization(ORGANIZATION_NAME)
        pass

    def tearDown(self):
        pass

    def test_info(self):
        assert self.org.info
        for key in FIELDS_ORGANIZATION:
            assert key in self.org.info

    def test_public_members(self):
        assert self.org.public_members
        assert len(self.org.public_members) > 0

        assert self.org.public_members[0]
        for key in FIELDS_USER:
            assert key in self.org.public_members[0].info

    def test_repos(self):
        assert self.org.repos
        assert len(self.org.repos) > 0

        assert self.org.repos[0]
        for key in FIELDS_REPO:
            assert key in self.org.repos[0].info
