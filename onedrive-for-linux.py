#!/usr/bin/python3

from onedrive import Onedrive

onedrive = Onedrive()
onedrive.new_access_token()
print(onedrive.access_token)
onedrive.redeem_token()
print(onedrive.authorization_code)