
import json
import re
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPSConnection

class OAuth2Handler(BaseHTTPRequestHandler):
    def __send_answer(self, html_file):
        try:
            with open(html_file) as fd:
                content = fd.read()
                self.wfile.write(content.encode())
        except IOError as err:
            message = 'Whooops! ' + str(err)
            self.wfile.write(message.encode())

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        exp = re.search(r'[?&]code=([^&]+).*$', self.path)
        if (exp != None):
            self.server.access_token = exp.group().split('=')[1]
            self.__send_answer("www/success.html")
        else:
            self.__send_answer("www/error.html")

    def log_message(self, format, *args):
        return

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

    def new_access_token(self):
        url = (Onedrive.AUTH_URL + "?client_id=" + Onedrive.CLIENT_ID + "&scope=" + Onedrive.SCOPES + 
               "&response_type=code&redirect_uri=" + Onedrive.REDIRECT_URL)
        webbrowser.open(url)
        server = HTTPServer(('localhost', 8000), OAuth2Handler)
        server.handle_request()
        self.access_token = server.access_token
    
    def redeem_token(self):
        body = 'client_id=' + Onedrive.CLIENT_ID + '&code=' + self.access_token + '&grant_type=authorization_code'
        conn = HTTPSConnection('login.microsoftonline.com')
        conn.request('POST', '/common/oauth2/v2.0/token', body)
        response = json.load(conn.getresponse())
        self.authorization_code = response['access_token']
