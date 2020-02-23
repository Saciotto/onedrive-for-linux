#!/usr/bin/python3

from onedrive import Onedrive

onedrive = Onedrive()
onedrive.login()
print(onedrive._access_token)