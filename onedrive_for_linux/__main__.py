
from .onedrive import Onedrive
from .cli_login import onedrive_login
from .onedrive_account import OnedriveAccount
from .onedrive_account_db import OnedriveAccountDB

my_account = None

with OnedriveAccountDB() as db:
    accounts = db.load_all()
    print(accounts)
    print(type(accounts))

    for account in accounts:
        if account[1] == "Matheus Rossi Saciotto":
            my_account = account

if not my_account:
    onedrive = onedrive_login()
    account = OnedriveAccount(onedrive)
else:
    account = OnedriveAccount.from_database(my_account)

print(account)

default_drive =  account.onedrive.get_defualt_drive()
drive_id = default_drive['id']
print(drive_id)

default_root = account.onedrive.get_defualt_root()
file_id = default_root['id']
print(file_id)

delta = account.onedrive.view_changes_by_id(drive_id, file_id)
with open('delta.json', 'w') as fp:
    print(delta, file=fp)

with open('results.txt', 'w') as fp:
    print('Changes by path root:', account.onedrive.view_changes_by_path(), file=fp)

with OnedriveAccountDB() as db:
    db.save(account.to_database())