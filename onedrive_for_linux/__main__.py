from argparse import ArgumentParser

APP_NAME = 'OneDrive'
APP_VERSION = '1.0.0'


def login(args):
    print('Function Login')


def download(args):
    print('Function Donwload')


def logout(args):
    print('Function Logout')


def monitor(args):
    print('Function Monitor')


def print_token(args):
    print('Function Print Token')


def resync(args):
    print('Function Resync')


parser = ArgumentParser(prog=APP_NAME)
subparsers = parser.add_subparsers(title='commands', metavar='command', help='description')

subparser = subparsers.add_parser('login', help='login a new user')
subparser.set_defaults(func=login)

subparser = subparsers.add_parser('download', help='only download remote changes')
subparser.set_defaults(func=download)

subparser = subparsers.add_parser('logout', help='logout the current user')
subparser.set_defaults(func=logout)

subparser = subparsers.add_parser('monitor', help='keep monitoring for local and remote changes')
subparser.set_defaults(func=monitor)

subparser = subparsers.add_parser('token', help='print the access token, useful for debugging')
subparser.set_defaults(func=print_token)

subparser = subparsers.add_parser('resync', help='forget the last saved state, perform a full sync')
subparser.set_defaults(func=resync)

parser.add_argument('--verbose', help='Print more details, useful for debugging', action='store_true')
parser.add_argument('--version', action='version', version=f'{APP_NAME} {APP_VERSION}')

args = parser.parse_args()
args.func(args)

# from .cli_login import onedrive_login
# from .onedrive import Onedrive
# from .onedrive_account import OnedriveAccount
# from .onedrive_account_db import OnedriveAccountDB
#
# def perform_sync():
#     print('Perform sync')
#
# account_db = None
#
# with OnedriveAccountDB() as db:
#     accounts = db.load_all()
#     if len(accounts) > 0:
#         account_db = accounts[0]
#
# if not account_db:
#     onedrive = onedrive_login()
#     account = OnedriveAccount(onedrive)
# else:
#     account = OnedriveAccount.from_database(account_db)
#
# perform_sync()
