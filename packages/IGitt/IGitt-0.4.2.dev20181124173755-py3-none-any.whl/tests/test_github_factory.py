import os

from tests import IGittTestCase
from IGitt.factory import get_repo
from IGitt.GitHub import GitHubToken
from IGitt.GitHub import GitHubJsonWebToken
from IGitt.GitHub import GitHubInstallationToken


class SuccessfulGitHubFactoryTest(IGittTestCase):

    def setUp(self):
        self.url = 'https://github.com/gitmate-test-user/test.git'
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.wallet = [self.token]
        self.repo = get_repo(self.url, self.wallet)
        jwt = GitHubJsonWebToken(os.environ['GITHUB_PRIVATE_KEY'],
                                 int(os.environ['GITHUB_TEST_APP_ID']))
        self.install_token = GitHubInstallationToken(473693, jwt)
        self.wallet.insert(0, self.install_token)
        self.install_repo = get_repo(self.url, self.wallet)

    def test_id(self):
        self.assertEqual(self.repo.identifier, 49558751)
        self.assertEqual(self.install_repo.identifier, 49558751)

    def test_hoster(self):
        self.assertEqual(self.repo.hoster, 'github')
        self.assertEqual(self.install_repo.hoster, 'github')

    def test_full_name(self):
        self.assertEqual(self.repo.full_name, 'gitmate-test-user/test')
        self.assertEqual(self.install_repo.full_name, 'gitmate-test-user/test')
