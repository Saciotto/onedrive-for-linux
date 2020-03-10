import json
import webbrowser
from http.server import HTTPServer
from datetime import datetime, timedelta
from urllib.request import Request, urlopen

from .oauth2_handler import OAuth2Handler
from .exceptions import LoginException

# Applicaton
CLIENT_ID = 'c22bd74f-da4c-460d-af0a-f97aa232a908'
SCOPES = 'Files.ReadWrite%20Files.ReadWrite.all%20Sites.ReadWrite.All%20offline_access'
REDIRECT_URL = 'http://localhost:8000'
SELECT_CHANGES = '?select=id,name,eTag,cTag,deleted,file,folder,root,fileSystemInfo,remoteItem,parentReference'

# Microsoft Authorization
AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# Microsoft Graph API
DRIVE_URL = 'https://graph.microsoft.com/v1.0/me/drive'
ITEM_BY_ID_URL = 'https://graph.microsoft.com/v1.0/me/drive/items/'
ITEM_BY_PATH_URL = 'https://graph.microsoft.com/v1.0/me/drive/root:/'
DRIVE_BY_ID_URL = 'https://graph.microsoft.com/v1.0/drives/'

def onedrive_login():
    url = f'{AUTH_URL}?client_id={CLIENT_ID}&scope={SCOPES}&response_type=code&redirect_uri={REDIRECT_URL}'
    webbrowser.open(url)
    server = HTTPServer(('localhost', 8000), OAuth2Handler)
    server.handle_request()
    code = getattr(server, 'code', None)
    if not code:
        raise LoginException("User authorization failed")
    return OnedriveApi(code)

class OnedriveApi:

    def __init__(self, account):
        self._timeout = 5
        if type(account) == tuple:
            self._drive_id, self._user, self._access_token, self._refresh_token, expire_date = account
            self._expire_date = datetime.fromisoformat(expire_date)
        else:
            self._redeem_token(account)
            self._get_user()

    def __str__(self):
        return f'ID: "{self._drive_id}", OneDrive user: "{self._user}"'

    def get_account(self):
        return (self._drive_id, self._user, self._access_token, self._refresh_token, self._expire_date.isoformat(' '))

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/drive_get
    def get_defualt_drive(self):
        self._validate_token()
        url = DRIVE_URL
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self._timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get
    def get_defualt_root(self):
        self._validate_token()
        url = f'{DRIVE_URL}/root'
        headers = headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self._timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delta
    def view_changes_by_id(self, drive_id, file_id, url=None):
        self._validate_token()
        if not url:
            url = f'{DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/delta'
            url += SELECT_CHANGES
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self._timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delta
    def view_changes_by_path(self, path=None, url=None):
        self._validate_token()
        if(not url):
            if not path or path == '.':
                url = f'{DRIVE_URL}/root/delta'
            else:
                url = f'{ITEM_BY_PATH_URL}/{path}:delta'
            url += SELECT_CHANGES
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self._timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get_content
    def download_by_id(self, drive_id, file_id, filename):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content?AVOverride=1'
        with open(filename, 'wb+') as fp:
            headers = {'Authorization': self._access_token}
            request = Request(url, headers=headers)
            with urlopen(request, timeout=self._timeout) as response:
                fp.write(response.read())

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content
    def simple_upload(self, local_path, parent_drive_id, parent_id, filename, e_tag = None):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}:/{filename}:/content'
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            request = Request(url, headers=headers, data=data, method='PUT')
            with urlopen(request) as response:
                return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content
    def simple_upload_replace(self, local_path, drive_id, file_id, e_tag=None):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content'
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            request = Request(url, headers=headers, data=data, method='PUT')
            with urlopen(request) as response:
                return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_update
    def update_by_id(self, drive_id, file_id, data, e_tag=None):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        if (e_tag):
            headers['If-Match'] = e_tag
        request = Request(url, headers=headers, data=data, method='PATCH')
        with urlopen(request) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delete
    def delete_by_id(self, drive_id, file_id, e_tag=None):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
        headers = {'Authorization': self._access_token}
        if (e_tag):
            headers['If-Match'] = e_tag
        request = Request(url, headers=headers, method='DELETE')
        with urlopen(request) as _:
            pass

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_post_children
    def create_by_id(self, parent_drive_id, parent_id, item):
        self._validate_token()
        url = f'{DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}/children'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        request = Request(url, data=item.encode(), headers=headers, method='POST')
        with urlopen(request) as response:
            return json.load(response)

    def create_upload_session(self, parent_drive_dd, parent_id, filename, e_tag):
        pass

    def upload_fragment(self, upload_url, filepath, offset, offset_size, filesize):
        pass

    def request_upload_status(self, upload_url):
        pass

    def _get_user(self):
        response = self.get_defualt_drive()
        self._drive_id = response['id']
        self._user = response['owner']['user']['displayName']
    
    def _redeem_token(self, code):
        body = f'client_id={CLIENT_ID}&code={code}&grant_type=authorization_code'
        self._acquire_token(body)

    def _validate_token(self):
        now = datetime.now()
        if (self._expire_date >= now):
            self._renew_token()

    def _renew_token(self):
        body = f'client_id={CLIENT_ID}&refresh_token={self._refresh_token}&grant_type=refresh_token'
        self._acquire_token(body)

    def _acquire_token(self, body):
        now = datetime.now()
        request = Request(TOKEN_URL, data=body.encode(), method='POST')
        with urlopen(request) as response:
            data = json.load(response)
            try:
                self._access_token = data['access_token']
                self._refresh_token = data['refresh_token']
                expire = data['expires_in']
            except Exception as e:
                print('Login Error:', e)
                raise LoginException('Redeem access token failed')
            self._expire_date = now + timedelta(seconds=int(expire))
