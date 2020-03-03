import json
import webbrowser
from http.server import HTTPServer
from http.client import HTTPSConnection
from oauth2_handler import OAuth2Handler
from exceptions import LoginException
from datetime import datetime, timedelta
from urllib import request

class OnedriveApi:
    CLIENT_ID = "c22bd74f-da4c-460d-af0a-f97aa232a908"
    AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    REDIRECT_URL = "http://localhost:8000"
    TOKEN_URL = "https://login.microsoftonline.com"
    DRIVE_URL = "https://graph.microsoft.com/v1.0/me/drive"
    ITEM_BY_ID_URL = "https://graph.microsoft.com/v1.0/me/drive/items/"
    ITEM_BY_PATH_URL = "https://graph.microsoft.com/v1.0/me/drive/root:/"
    DRIVE_BY_ID_URL = "https://graph.microsoft.com/v1.0/drives/"
    SCOPES = "Files.ReadWrite%20Files.ReadWrite.all%20Sites.ReadWrite.All%20offline_access"

    def __init__(self):
        self._code = None
        self._access_token = None
        self._expire_date = None
        self._refresh_token = None
        self._logged = False

    def login(self):
        self._ask_permission()
        self._redeem_token()
        self._logged = True

    def get_defualt_drive(self):
        self._validate_login()
        headers = {"Authorization": self._access_token}
        conn = HTTPSConnection('graph.microsoft.com') 
        conn.request('GET', '/v1.0/me/drive', headers=headers)
        return json.load(conn.getresponse())

    def get_defualt_root(self):
        self._validate_login()
        headers = {"Authorization": self._access_token}
        conn = HTTPSConnection('graph.microsoft.com') 
        conn.request('GET', '/v1.0/me/drive/root', headers=headers)
        return json.load(conn.getresponse())
    
    def view_changes_by_id(self, drive_id, file_id, url=None):
        self._validate_login()
        if(not url):
            url = '/v1.0/drives/' + drive_id + '/items/' + file_id + '/delta'
            url += '?select=id,name,eTag,cTag,deleted,file,folder,root,fileSystemInfo,remoteItem,parentReference'
            print(url)
        headers = {'Authorization': self._access_token}
        conn = HTTPSConnection('graph.microsoft.com') 
        conn.request('GET', url, headers=headers)
        return json.load(conn.getresponse())

    def view_changes_by_path(self, path=None, url=None):
        self._validate_login()
        if(not url):
            if (path == None):
                url = '/v1.0/me/drive/root/delta'
            else:
                url = '/v1.0/me/drive/root:/' + path + ':delta'
            url += '?select=id,name,eTag,cTag,deleted,file,folder,root,fileSystemInfo,remoteItem,parentReference'
        headers = {'Authorization': self._access_token}
        conn = HTTPSConnection('graph.microsoft.com') 
        conn.request('GET', url, headers=headers)
        return json.load(conn.getresponse())

    def download_by_id(self, drive_id, file_id, filename):
        self._validate_login()
        url = 'https://graph.microsoft.com//v1.0/drives/' + drive_id + '/items/' + file_id + '/content?AVOverride=1'
        with open(filename, 'wb+') as fp:
            headers = {'Authorization': self._access_token}
            req = request.Request(url, headers=headers)
            with request.urlopen(req) as f:
                fp.write(f.read())

    def simple_upload(self, local_path, parent_drive_id, parent_id, filename, e_tag = None):
        self._validate_login()
        url = ('https://graph.microsoft.com/v1.0/drives/' + parent_drive_id + '/items/' + parent_id + ':/' +
                filename + ':/content')
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            req = request.Request(url, headers=headers, data=data, method='PUT')
            with request.urlopen(req) as _:
                pass

    def simple_upload_replace(self, local_path, drive_id, file_id, e_tag=None):
        self._validate_login()
        url = ('https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/' + file_id + '/content')
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            req = request.Request(url, headers=headers, data=data, method='PUT')
            with request.urlopen(req) as _:
                pass

    def update_by_id(self, drive_id, file_id, data, e_tag=None):
        self._validate_login()
        url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/' + file_id
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        if (e_tag):
            headers['If-Match'] = e_tag

        req = request.Request(url, headers=headers, data=data, method='PATCH')
        with request.urlopen(req) as _:
            pass

    def delete_by_id(self, drive_id, file_id, e_tag=None):
        self._validate_login()
        url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/' + file_id
        headers = {'Authorization': self._access_token}
        if (e_tag):
            headers['If-Match'] = e_tag

        req = request.Request(url, headers=headers, method='DELETE')
        with request.urlopen(req) as _:
            pass

    def create_by_id(self, parent_drive_id, parent_id, item):
        self._validate_login()
        url = 'https://graph.microsoft.com/v1.0/drives/' + parent_drive_id + '/items/' + parent_id + '/children'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        req = request.Request(url, data=item.encode(), headers=headers, method='POST')
        with request.urlopen(req) as _:
            pass

    def create_upload_session(self, parent_drive_dd, parent_id, filename, e_tag):
        pass

    def upload_fragment(self, upload_url, filepath, offset, offset_size, filesize):
        pass

    def request_upload_status(self, upload_url):
        pass

    def _ask_permission(self):
        url = (f'{OnedriveApi.AUTH_URL}?client_id={OnedriveApi.CLIENT_ID}&scope={OnedriveApi.SCOPES}'
               f"&response_type=code&redirect_uri={OnedriveApi.REDIRECT_URL}")
        webbrowser.open(url)
        server = HTTPServer(('localhost', 8000), OAuth2Handler)
        server.handle_request()
        self._code = getattr(server, 'code', None)
        if (not self._code):
            raise LoginException("User authorization failed")
    
    def _redeem_token(self):
        body = f'client_id={OnedriveApi.CLIENT_ID}&code={self._code}&grant_type=authorization_code'
        self._acquire_token(body)

    def _renew_token(self):
        body = f'client_id={OnedriveApi.CLIENT_ID}&refresh_token={self._refresh_token}&grant_type=refresh_token'
        self._acquire_token(body)

    def _acquire_token(self, body):
        now = datetime.now()

        conn = HTTPSConnection('login.microsoftonline.com')
        conn.request('POST', '/common/oauth2/v2.0/token', body)

        response = json.load(conn.getresponse())
        self._access_token = response.get('access_token', None)
        self._refresh_token = response.get('refresh_token', None)
        expire = response.get('expires_in', 0)
        self._expire_date = now + timedelta(seconds=int(expire))

        if (not self._access_token or not expire or not self._refresh_token):
            raise LoginException("Redeem access token failed")

    def _ensure_logged(self):
        if (not self._logged):
            raise LoginException("User must be logged in")

    def _is_token_expired(self):
        now = datetime.now()
        return (self._expire_date >= now)

    def _validate_login(self):
        self._ensure_logged()
        if (self._is_token_expired()):
            self._renew_token()
