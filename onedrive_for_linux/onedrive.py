import json
from datetime import datetime, timedelta
from urllib.request import Request, urlopen

from . import routes
from .exceptions import LoginException

class Onedrive:

    DEFAULT_TIMEOUT = 5 

    def __init__(self, access_token, refresh_token, expire_date):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expire_date = expire_date
        self.timeout = Onedrive.DEFAULT_TIMEOUT

    @staticmethod
    def login(auth_code):
        access_token, refresh_token, expire_date = Onedrive._redeem_token(auth_code)
        return Onedrive(access_token, refresh_token, expire_date)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/drive_get
    def get_defualt_drive(self):
        self._renew_token()
        url = routes.DRIVE_URL
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get
    def get_defualt_root(self):
        self._renew_token()
        url = f'{routes.DRIVE_URL}/root'
        headers = headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delta
    def view_changes_by_id(self, drive_id, file_id, url=None):
        self._renew_token()
        if not url:
            url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/delta'
            url += routes.SELECT_CHANGES
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delta
    def view_changes_by_path(self, path=None, url=None):
        self._renew_token()
        if(not url):
            if not path or path == '.':
                url = f'{routes.DRIVE_URL}/root/delta'
            else:
                url = f'{routes.ITEM_BY_PATH_URL}/{path}:delta'
            url += routes.SELECT_CHANGES
        headers = {'Authorization': self._access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get_content
    def download_by_id(self, drive_id, file_id, filename):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content?AVOverride=1'
        with open(filename, 'wb+') as fp:
            headers = {'Authorization': self._access_token}
            request = Request(url, headers=headers)
            with urlopen(request, timeout=self.timeout) as response:
                fp.write(response.read())

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content
    def simple_upload(self, local_path, parent_drive_id, parent_id, filename, e_tag = None):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}:/{filename}:/content'
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            request = Request(url, headers=headers, data=data, method='PUT')
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content
    def simple_upload_replace(self, local_path, drive_id, file_id, e_tag=None):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content'
        headers = {'Authorization': self._access_token, "Content-Type": "application/octet-stream"}
        if (e_tag):
            headers['If-Match'] = e_tag
        with open(local_path, 'rb') as fp:
            data = fp.read()
            request = Request(url, headers=headers, data=data, method='PUT')
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_update
    def update_by_id(self, drive_id, file_id, data, e_tag=None):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        if (e_tag):
            headers['If-Match'] = e_tag
        request = Request(url, headers=headers, data=data, method='PATCH')
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_delete
    def delete_by_id(self, drive_id, file_id, e_tag=None):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
        headers = {'Authorization': self._access_token}
        if (e_tag):
            headers['If-Match'] = e_tag
        request = Request(url, headers=headers, method='DELETE')
        with urlopen(request, timeout=self.timeout) as _:
            pass

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_post_children
    def create_by_id(self, parent_drive_id, parent_id, item):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}/children'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        request = Request(url, data=item.encode(), headers=headers, method='POST')
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_createuploadsession
    def create_upload_session(self, parent_drive_id, parent_id, filename, e_tag=None):
        self._renew_token()
        url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}:/{filename}:/createUploadSession'
        headers = {'Authorization': self._access_token, "Content-Type": "application/json"}
        if (e_tag):
            headers['If-Match'] = e_tag
        request = Request(url, headers=headers, method='POST')
        with urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_createuploadsession?view=odsp-graph-online
    def upload_fragment(self, upload_url, local_path, offset, content_size, filesize):
        self._renew_token()
        content_range = f'bytes {offset}-{offset + content_size - 1}/{filesize}'
        headers = {'Content-range': content_range}
        with open(local_path, 'rb') as fp:
            fp.seek(offset)
            data = fp.read(content_size)
            request = Request(upload_url, headers=headers, data=data, method='PUT')
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)

    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_createuploadsession?view=odsp-graph-online
    def request_upload_status(self, upload_url):
        self._renew_token()
        with urlopen(upload_url, timeout=self.timeout) as response:
            return json.load(response)

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def expire_date(self):
        return self._expire_date

    def _renew_token(self):
        if self._expire_date <= datetime.now():
            body = f'client_id={routes.CLIENT_ID}&refresh_token={self._refresh_token}&grant_type=refresh_token'
            self._access_token, self._refresh_token, self._expire_date = Onedrive._acquire_token(body, self.timeout)

    @staticmethod
    def _redeem_token(code):
        body = f'client_id={routes.CLIENT_ID}&code={code}&grant_type=authorization_code'
        return Onedrive._acquire_token(body)

    @staticmethod
    def _acquire_token(body, timeout=Onedrive.DEFAULT_TIMEOUT):
        now = datetime.now()
        request = Request(routes.TOKEN_URL, data=body.encode(), method='POST')
        with urlopen(request, timeout=timeout) as response:
            data = json.load(response)
            try:
                access_token = data['access_token']
                refresh_token = data['refresh_token']
                expire = data['expires_in']
            except Exception as e:
                print('Login Error:', e)
                raise LoginException('Redeem access token failed')
            expire_date = now + timedelta(seconds=int(expire))
        return access_token, refresh_token, expire_date
