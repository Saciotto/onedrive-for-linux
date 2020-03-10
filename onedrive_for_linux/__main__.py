
from .onedrive_api import OnedriveApi, onedrive_login
from .database import Database

my_account = None
with Database() as db:
    accounts = db.load_all_accounts()
    print(accounts)
    print(type(accounts))
    for account in accounts:
        if account[1] == "Matheus Rossi Saciotto":
            my_account = account

if not my_account:
    onedrive = onedrive_login()
    account = onedrive.get_account()
else:
    onedrive = OnedriveApi(my_account)
    my_account = onedrive.get_account()

with Database() as db:
    db.save_account(account)

onedrive = OnedriveApi(account)

print(account)

default_drive =  onedrive.get_defualt_drive()
drive_id = default_drive['id']
print(drive_id)

default_root = onedrive.get_defualt_root()
default_root = onedrive.get_defualt_root()
file_id = default_root['id']
print(file_id)

delta = onedrive.view_changes_by_id(drive_id, file_id)
with open('delta.json', 'w') as fp:
    print(delta, file=fp)

with open('results.txt', 'w') as fp:
    print('Changes by path root:', onedrive.view_changes_by_path(), file=fp)