import logging
from argparse import ArgumentParser

from psync.onedrive.account import OnedriveAccount
from psync.onedrive import accounts

APP_VERSION = '1.0.0'

def login(args):
    account = OnedriveAccount.webbrowser_login(args.name)
    accounts.add(account)

def logout(args):
    accounts.remove(args.name)

def users(args):
    users = accounts.users()
    for user in users:
        print(user)

parser = ArgumentParser(prog='psycn')
subparsers = parser.add_subparsers(title='commands', metavar='command', help='description')

subparser = subparsers.add_parser('login', help='Performs a new user login')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=login)

subparser = subparsers.add_parser('users', help='Shows a list of logged users')
subparser.set_defaults(func=users)

subparser = subparsers.add_parser('logout', help='Removes the user from syncing')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=logout)


parser.add_argument('-v', '--verbose', help='Print more details, useful for debugging', action='store_true')
parser.add_argument('--version', action='version', version=f'OneDive {APP_VERSION}')

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

args.func(args)
