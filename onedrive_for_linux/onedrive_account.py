from datetime import datetime

from .onedrive import Onedrive

class OnedriveAccount:

    def __init__(self, onedrive, account_id=None):
        self.onedrive = onedrive
        if account_id:
            self.drive_id, self.name = account_id
        else:
            self.use_default_id()
        
    def __str__(self):
        return f'ID: "{self.drive_id}", OneDrive user: "{self.name}"'

    @staticmethod
    def from_database(data):
        drive_id, name, access_token, refresh_token, expire_date = data
        expire_date = datetime.fromisoformat(expire_date)
        onedrive = Onedrive(access_token, refresh_token, expire_date)
        account_id = (drive_id, name)
        return OnedriveAccount(onedrive, account_id)

    def to_database(self):
        access_token = self.onedrive.access_token
        refresh_token = self.onedrive.refresh_token
        expire_date = self.onedrive.expire_date.isoformat(' ')
        return (self.drive_id, self.name, access_token, refresh_token, expire_date)

    def use_default_id(self):
        response = self.onedrive.get_defualt_drive()
        self.drive_id = response['id']
        self.name = response['owner']['user']['displayName']
