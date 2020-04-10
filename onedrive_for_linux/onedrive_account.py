from datetime import datetime

from .onedrive import Onedrive
from .onedrive_account_db import OnedriveAccountDB


class OnedriveAccount:

    def __init__(self, account_id, onedrive):
        self.account_id = account_id
        self.onedrive = onedrive

    def __str__(self):
        return f'OndriveAccount({self.account_id})"'

    def save(self):
        with OnedriveAccountDB() as db:
            db.save(self.to_database())

    @staticmethod
    def load(name):
        with OnedriveAccountDB() as db:
            account_db = db.load(name)
        return OnedriveAccount.from_database(account_db)

    @staticmethod
    def from_database(data):
        account_id, access_token, refresh_token, expire_date = data
        expire_date = datetime.fromisoformat(expire_date)
        onedrive = Onedrive(access_token, refresh_token, expire_date)
        return OnedriveAccount(account_id, onedrive)

    def to_database(self):
        access_token = self.onedrive.access_token
        refresh_token = self.onedrive.refresh_token
        expire_date = self.onedrive.expire_date.isoformat(' ')
        return (self.account_id, access_token, refresh_token, expire_date)
