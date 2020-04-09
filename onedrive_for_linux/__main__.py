from .cli_login import onedrive_login
from .onedrive import Onedrive
from .onedrive_account import OnedriveAccount
from .onedrive_account_db import OnedriveAccountDB


def perform_sync():
    print('Perform sync')

account_db = None

with OnedriveAccountDB() as db:
    accounts = db.load_all()
    if len(accounts) > 0:
        account_db = accounts[0]

if not account_db:
    onedrive = onedrive_login()
    account = OnedriveAccount(onedrive)
else:
    account = OnedriveAccount.from_database(account_db)

perform_sync()
