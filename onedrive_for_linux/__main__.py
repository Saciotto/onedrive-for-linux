
from .onedrive_api import OnedriveApi, onedrive_login

onedrive2 = onedrive_login()
account = onedrive2.get_account()

onedrive = OnedriveApi(account)

default_drive =  onedrive.get_defualt_drive()
drive_id = default_drive['id']
print(drive_id)

default_root = onedrive.get_defualt_root()
file_id = default_root['id']
print(file_id)

delta = onedrive.view_changes_by_id(drive_id, file_id)
with open('delta.json', 'w') as fp:
    print(delta, file=fp)

with open('results.txt', 'w') as fp:
    print('Changes by path root:', onedrive.view_changes_by_path(), file=fp)