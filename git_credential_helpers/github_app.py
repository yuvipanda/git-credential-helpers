#!/usr/bin/env python3
"""
git-credential helper for accessing private GitHub repositories

[GitHub Apps](https://docs.github.com/en/free-pro-team@latest/developers/apps)
can provide fine grained, per-repository access control. This helper lets
git automatically create GitHub app installation tokens for interacting
with private repos that have the GitHub app installed.
"""
import github3
import sys
import argparse

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--app-key-file',
        help='Path to RSA private key file of the GitHub app',
        required=True,
        type=argparse.FileType('r')
    )
    argparser.add_argument(
        '--app-id',
        help='GitHub app id',
        type=int,
        required=True
    )
    argparser.add_argument(
        'operation',
        # We don't want to print to stderr when 'store' or 'erase'
        # are passed to the script. So we accept all possibilities,
        # but only respond to 'get'
        choices=['get', 'store', 'erase'],
        help='git credential operation to perform. Only get is supported',
    )

    args = argparser.parse_args()

    if args.operation != 'get':
        # This isn't a persistent credential helper, so we don't support store or erase
        sys.exit(1)

    # Parse '=' delimited input via stdin
    # Documented at https://git-scm.com/docs/git-credential#IOFMT
    keys = {}
    for l in sys.stdin:
        parts = l.strip().split('=', 1)
        keys[parts[0]] = parts[1]


    # Password for cloning a repo is based on the organization / user that
    # has installed the GitHub app.
    user, repo = keys['path'].split('/', 1)

    # Authenticate to GitHub as our App, using the private RSA key & identifier
    gh = github3.github.GitHub()

    app_private_key = args.app_key_file.read()
    app_identifier = args.app_id
    gh.login_as_app(app_private_key.encode(), app_identifier)


    # An app can have multiple 'installations', where each installation is
    # a user / org that has granted access to a specific set of repositories.
    # We assume that the app has been granted access to the private repo being
    # pulled. The installation's session token can be used as 'password' to do
    # git operations.
    #
    # We try fetch the installation for the given repo, and set session token as
    # password if the GitHub app is installed for the repo. We output nothing
    # otherwise, and git will move on to other credentials
    try:
        installation = gh.app_installation_for_repository(user, repo)
        gh.login_as_app_installation(app_private_key.encode(), app_identifier, installation.id)
        print(f'username=x-access-token')
        print(f'password={gh.session.auth.token}')
    except github3.exceptions.NotFoundError:
        pass

if __name__ == '__main__':
    main()
