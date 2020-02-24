#!/usr/bin/python3

from onedrive import Onedrive

onedrive = Onedrive()
onedrive.login()

print('Default drive:', onedrive.get_defualt_drive())
print('Default root:', onedrive.get_defualt_root())