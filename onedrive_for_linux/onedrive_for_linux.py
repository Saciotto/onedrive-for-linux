#!/usr/bin/python3

from onedrive import Onedrive

onedrive = Onedrive()
onedrive.login()

#print('Default drive:', onedrive.get_defualt_drive())
#print('Default root:', onedrive.get_defualt_root())

default_drive =  onedrive.get_defualt_drive()
drive_id = default_drive['id']
print(drive_id)

default_root = onedrive.get_defualt_root()
file_id = default_root['id']
print(file_id)


with open('results.txt', 'w+') as fp:
    print('Changes by id: ', onedrive.view_changes_by_id(drive_id, file_id))
    #print('Changes by path root:', onedrive.view_changes_by_path(), file=fp)