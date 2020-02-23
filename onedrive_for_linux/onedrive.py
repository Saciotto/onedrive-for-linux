import json
import webbrowser
from http.server import HTTPServer
from http.client import HTTPSConnection
from oauth2_handler import OAuth2Handler

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
        self.code = None
        self.access_token = None
        self.user_logged = False

    def ask_permission(self):
        url = (f'{Onedrive.AUTH_URL}?client_id={Onedrive.CLIENT_ID}&scope={Onedrive.SCOPES}'
               f"&response_type=code&redirect_uri={Onedrive.REDIRECT_URL}")
        webbrowser.open(url)
        server = HTTPServer(('localhost', 8000), OAuth2Handler)
        server.handle_request()
        server.code = None
        self.code = server.code
    
    def redeem_token(self):
        body = f'client_id={Onedrive.CLIENT_ID}&code={self.code}&grant_type=authorization_code'
        conn = HTTPSConnection('login.microsoftonline.com')
        conn.request('POST', '/common/oauth2/v2.0/token', body)
        response = json.load(conn.getresponse())
        self.access_token = response['access_token']
        print(response)
