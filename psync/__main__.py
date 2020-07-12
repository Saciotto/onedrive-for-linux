import logging
from argparse import ArgumentParser

from psync.sync.profile import Profile
from psync.sync import profiles
from psync.sync import config

APP_VERSION = '1.0.0'

def login(args):
    Profile.webbrowser_login(args.name)

def logout(args):
    profiles.remove(args.name)

def profile_list(args):
    profiles.print_all()

def set_default_profile(args):
    config.set_default_profile(args.name)

def print_default_profile(args):
    print(config.get_default_profile())

parser = ArgumentParser(prog='psycn')
subparsers = parser.add_subparsers(title='commands', metavar='command', help='description')

subparser = subparsers.add_parser('login', help='Performs a new user login')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=login)

subparser = subparsers.add_parser('list', help='Shows a list of logged users')
subparser.set_defaults(func=profile_list)

subparser = subparsers.add_parser('remove', help='Removes the user from syncing')
subparser.add_argument('name', help='unique name for this account')
subparser.set_defaults(func=logout)

subparser = subparsers.add_parser('default', help='')
subparser.add_argument('name')
subparser.set_defaults(func=set_default_profile)

subparser = subparsers.add_parser('show-default', help='')
subparser.set_defaults(func=print_default_profile)

parser.add_argument('-v', '--verbose', help='Print more details, useful for debugging', action='store_true')
parser.add_argument('--version', action='version', version=f'OneDive {APP_VERSION}')

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

args.func(args)
