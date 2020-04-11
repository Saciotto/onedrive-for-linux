import webbrowser
from http.server import HTTPServer

from onedrive_for_linux.util import routes
from onedrive_for_linux.util.oauth2_handler import OAuth2Handler
from onedrive_for_linux.models.onedrive_account import OnedriveAccount


def onedrive_login(name):
    url = f'{routes.AUTH_URL}?client_id={routes.CLIENT_ID}&scope={routes.SCOPES}&response_type=code&redirect_uri={routes.REDIRECT_URL}'
    webbrowser.open(url)
    server = HTTPServer(('localhost', 8000), OAuth2Handler)
    server.handle_request()
    code = getattr(server, 'code')
    return OnedriveAccount.login(name, code)
