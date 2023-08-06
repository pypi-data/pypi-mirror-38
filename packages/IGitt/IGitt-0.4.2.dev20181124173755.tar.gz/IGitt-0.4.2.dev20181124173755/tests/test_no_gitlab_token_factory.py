import os

from tests import IGittTestCase
from IGitt.factory import get_repo
from IGitt.GitHub import GitHubToken


class NoGitLabTokenFactoryTest(IGittTestCase):

    def setUp(self):
        self.url = 'https://gitlab.com/gitmate-test-user/test.git'
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.wallet = [self.token]

    def test_no_github_token(self):
        with self.assertRaises(AssertionError):
            get_repo(self.url, self.wallet)
