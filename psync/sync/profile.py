import os
from pathlib import Path

from psync.helpers.observer import Observer
from psync.onedrive.account import OnedriveAccount
from psync.onedrive import accounts
from psync.sync import profiles
            
class Profile(Observer):

    def __init__(self, profile_id, account, root_folder, name, username):
        self.profile_id = profile_id
        self.account = account
        self.root_folder = Path(root_folder)
        self.name = name
        self.username = username
        account.add_observer(self)

    @staticmethod
    def default_folder(profile_id):
        return Path.home() / 'psync' / 'OneDrive' / profile_id

    @staticmethod
    def webbrowser_login(profile_id, root_folder=None):
        if not root_folder:
            root_folder = Profile.default_folder(profile_id)
        account = OnedriveAccount.webbrowser_login(profile_id)
        user_info = account.get_user_info()
        name = user_info['displayName']
        username = user_info['userPrincipalName']
        profile = Profile(profile_id, account, root_folder, name, username)
        profile.save()
        return profile

    def save(self):
        profiles.save(self)
        accounts.save(self.account)

    def update(self, _):
        self.save()

    def __str__(self):
        return f'{self.profile_id}: {self.name} - {self.username} - {self.root_folder}'
