import os

from tests import IGittTestCase
from IGitt.factory import get_repo
from IGitt.GitLab import GitLabOAuthToken


class NoGitHubTokenFactoryTest(IGittTestCase):

    def setUp(self):
        self.url = 'https://github.com/gitmate-test-user/test.git'
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.wallet = [self.token]

    def test_no_github_token(self):
        with self.assertRaises(AssertionError):
            get_repo(self.url, self.wallet)
