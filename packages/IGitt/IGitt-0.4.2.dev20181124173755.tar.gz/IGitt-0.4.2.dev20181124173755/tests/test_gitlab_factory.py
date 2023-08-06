import os

from tests import IGittTestCase
from IGitt.factory import get_repo
from IGitt.GitLab import GitLabOAuthToken, GitLabPrivateToken


class SuccessfulGitLabFactoryTest(IGittTestCase):

    def setUp(self):
        self.url = 'https://gitlab.com/gitmate-test-user/test.git'
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.wallet = [self.token]
        self.repo = get_repo(self.url, self.wallet)
        self.fork_token = GitLabPrivateToken(
            os.environ.get('GITLAB_TEST_TOKEN_2', ''))
        self.wallet.insert(0, self.fork_token)
        self.fork_repo = get_repo(self.url, self.wallet)

    def test_id(self):
        self.assertEqual(self.repo.identifier, 3439658)
        self.assertEqual(self.fork_repo.identifier, 3439658)

    def test_hoster(self):
        self.assertEqual(self.repo.hoster, 'gitlab')
        self.assertEqual(self.fork_repo.hoster, 'gitlab')

    def test_full_name(self):
        self.assertEqual(self.repo.full_name, 'gitmate-test-user/test')
        self.assertEqual(self.fork_repo.full_name, 'gitmate-test-user/test')
