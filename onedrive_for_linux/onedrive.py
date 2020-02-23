import json
import webbrowser
from http.server import HTTPServer
from http.client import HTTPSConnection
from oauth2_handler import OAuth2Handler
from exceptions import LoginException
from datetime import datetime, timedelta

class Onedrive:
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

    def _ask_permission(self):
        url = (f'{Onedrive.AUTH_URL}?client_id={Onedrive.CLIENT_ID}&scope={Onedrive.SCOPES}'
               f"&response_type=code&redirect_uri={Onedrive.REDIRECT_URL}")
        webbrowser.open(url)
        server = HTTPServer(('localhost', 8000), OAuth2Handler)
        server.handle_request()
        self._code = getattr(server, 'code', None)
        if (not self._code):
            raise LoginException("User authorization failed")
    
    def _redeem_token(self):
        body = f'client_id={Onedrive.CLIENT_ID}&code={self._code}&grant_type=authorization_code'
        self._acquire_token(body)

    def _renew_token(self):
        body = f'client_id={Onedrive.CLIENT_ID}&refresh_token={self._refresh_token}&grant_type=refresh_token'
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
        self._ensure_logged()
        now = datetime.now()
        return (self._expire_date >= now)

    def _validate_token(self):
        if (self._is_token_expired()):
            self._renew_token()
