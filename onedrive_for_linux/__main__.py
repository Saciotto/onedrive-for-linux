import logging
from argparse import ArgumentParser

from . import version
from .cli_login import onedrive_login
from .onedrive_account import OnedriveAccount
from .sync import SyncEngine

def login(args):
    onedrive = onedrive_login()
    account = OnedriveAccount(args.name, onedrive)
    account.save()


def sync(args):
    account = OnedriveAccount.load(args.name)
    sync_engine = SyncEngine(account)
    sync_engine.apply_differences()


def download(args):
    print('Function Donwload')


def logout(args):
    print('Function Logout')


def monitor(args):
    print('Function Monitor')


def print_token(args):
    account = OnedriveAccount.load(args.name)
    print(account.onedrive.access_token)


def resync(args):
    print('Function Resync')


parser = ArgumentParser(prog='onedrive')
subparsers = parser.add_subparsers(title='commands', metavar='command', help='description')

subparser = subparsers.add_parser('login', help='login a new user')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=login)

subparser = subparsers.add_parser('logout', help='logout the current user')
subparser.set_defaults(func=logout)

subparser = subparsers.add_parser('sync', help='perform a full sync')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=sync)

subparser = subparsers.add_parser('download', help='only download remote changes')
subparser.set_defaults(func=download)

subparser = subparsers.add_parser('monitor', help='keep monitoring for local and remote changes')
subparser.set_defaults(func=monitor)

subparser = subparsers.add_parser('resync', help='forget the last saved state, perform a full sync')
subparser.set_defaults(func=resync)

subparser = subparsers.add_parser('token', help='print the access token, useful for debugging')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=print_token)

parser.add_argument('-v', '--verbose', help='Print more details, useful for debugging', action='store_true')
parser.add_argument('--version', action='version', version=f'OneDive {version.APP_VERSION}')

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

args.func(args)
