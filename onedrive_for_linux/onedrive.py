import json
import webbrowser
from http.server import HTTPServer
from http.client import HTTPSConnection
from oauth2_handler import OAuth2Handler
from exceptions import LoginException

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

    def login(self):
        self._ask_permission()
        self._redeem_token()

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
        conn = HTTPSConnection('login.microsoftonline.com')
        conn.request('POST', '/common/oauth2/v2.0/token', body)
        response = json.load(conn.getresponse())
        self._access_token = response.get('access_token', None)
        if (not self._access_token):
            raise LoginException("Redeem access token failed")
