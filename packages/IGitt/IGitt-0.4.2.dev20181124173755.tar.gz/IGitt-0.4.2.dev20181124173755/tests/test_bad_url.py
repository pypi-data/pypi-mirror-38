from tests import IGittTestCase
from IGitt.factory import get_repo


class BadUrlFactoryTest(IGittTestCase):

    def setUp(self):
        self.BB_url = 'https://bitbucket.org/siddhpant/test.git'

    def test_BB_url_fail(self):
        with self.assertRaises(AssertionError):
            get_repo(self.BB_url, [])
