"""
Factory function for returning new repository objects
"""

from typing import List, Union
from giturlparse import parse

from IGitt.GitHub import GitHubToken
from IGitt.GitHub import GitHubInstallationToken
from IGitt.GitHub.GitHubRepository import GitHubRepository
from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab import GitLabPrivateToken
from IGitt.GitLab.GitLabRepository import GitLabRepository


def get_repo (URL: str,
              wallet: List[Union[GitHubToken, GitHubInstallationToken,
                                 GitLabOAuthToken, GitLabPrivateToken]]
             ) -> Union[GitHubRepository, GitLabRepository]:
    """
    :param URL: URL of the repository.
    :param wallet: Wallet; contains tokens. A list containing the tokens.
    """

    url = parse(URL)

    assert (url.resource == 'github.com' or url.resource == 'gitlab.com'), \
            'Only GitHub and GitLab supported.'

    fullname = url.owner + '/' + url.name

    if url.resource == 'github.com':
        token = None
        for Token in wallet:
            if isinstance(Token, GitHubToken):
                token = Token
                break
            elif isinstance(Token, GitHubInstallationToken):
                token = Token
                break
        assert token is not None, 'GitHub token not found.'
        return GitHubRepository(token, fullname)

    elif url.resource == 'gitlab.com':
        token = None
        for Token in wallet:
            if isinstance(Token, GitLabOAuthToken):
                token = Token
                break
            elif isinstance(Token, GitLabPrivateToken):
                token = Token
                break
        assert token is not None, 'GitLab token not found.'
        return GitLabRepository(token, fullname)
