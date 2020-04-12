import webbrowser
from http.server import HTTPServer
from datetime import datetime, timezone

from onedrive.helpers import onedrive_api
from onedrive.helpers.subject import Subject
from onedrive.helpers.oauth2_handler import OAuth2Handler


class OnedriveAccount(Subject):

    def __init__(self, account_id, access_token, refresh_token, expire_date):
        super().__init__()
        self.__account_id = account_id
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        self.__expire_date = expire_date

    def __str__(self):
        return f'OndriveAccount({self.account_id})"'

    @staticmethod
    def login(account_id, code):
        access_token, refresh_token, expire_date = onedrive_api.redeem_token(code)
        return OnedriveAccount(account_id, access_token, refresh_token, expire_date)

    @staticmethod
    def webbrowser_login(name):
        url = (f'{onedrive_api.AUTH_URL}?client_id={onedrive_api.CLIENT_ID}&scope={onedrive_api.SCOPES}' +
               f'&response_type=code&redirect_uri={onedrive_api.REDIRECT_URL}')
        webbrowser.open(url)
        server = HTTPServer(('localhost', 8000), OAuth2Handler)
        server.handle_request()
        code = getattr(server, 'code')
        return OnedriveAccount.login(name, code)

    @property
    def access_token(self):
        return self.__access_token

    @property
    def account_id(self):
        return self.__account_id

    @property
    def refresh_token(self):
        return self.__refresh_token

    @property
    def expire_date(self):
        return self.__expire_date

    def get_defualt_drive(self):
        self._renew_token()
        return onedrive_api.get_defualt_drive(self.access_token)

    def get_defualt_root(self):
        self._renew_token()
        return onedrive_api.get_defualt_root(self.access_token)

    def view_changes_by_id(self, drive_id, file_id, url=None):
        self._renew_token()
        return onedrive_api.view_changes_by_id(self.access_token, drive_id, file_id, url)

    def view_changes_by_path(self, path=None, url=None):
        self._renew_token()
        return onedrive_api. view_changes_by_path(self.access_token, path, url)

    def download_by_id(self, drive_id, file_id, filename):
        self._renew_token()
        return onedrive_api.download_by_id(self.access_token, drive_id, file_id, filename)

    def simple_upload(self, local_path, parent_drive_id, parent_id, filename, e_tag=None):
        self._renew_token()
        return onedrive_api.simple_upload(self.access_token, local_path, parent_drive_id, parent_id, filename, e_tag)

    def simple_upload_replace(self, local_path, drive_id, file_id, e_tag=None):
        self._renew_token()
        return onedrive_api.simple_upload_replace(self.access_token, local_path, drive_id, file_id, e_tag)

    def update_by_id(self, drive_id, file_id, data, e_tag=None):
        self._renew_token()
        return onedrive_api.update_by_id(self.access_token, drive_id, file_id, data, e_tag)

    def delete_by_id(self, drive_id, file_id, e_tag=None):
        self._renew_token()
        onedrive_api.delete_by_id(self.access_token, drive_id, file_id, e_tag)

    def create_by_id(self, parent_drive_id, parent_id, item):
        self._renew_token()
        return onedrive_api.create_by_id(self.access_token, parent_drive_id, parent_id, item)

    def create_upload_session(self, parent_drive_id, parent_id, filename, e_tag=None):
        self._renew_token()
        return onedrive_api.create_upload_session(self.access_token, parent_drive_id, parent_id, filename, e_tag)

    def upload_fragment(self, upload_url, local_path, offset, content_size, filesize):
        self._renew_token()
        return onedrive_api.upload_fragment(upload_url, local_path, offset, content_size, filesize)

    def request_upload_status(self, upload_url):
        self._renew_token()
        return onedrive_api.request_upload_status(upload_url)

    def _renew_token(self):
        if self.__expire_date <= datetime.now(tz=timezone.utc):
            self.__access_token, self.__refresh_token, self.__expire_date = onedrive_api.renew_token(self.refresh_token)
            self.notify()
