import webbrowser
from http.server import HTTPServer

from . import routes
from .oauth2_handler import OAuth2Handler
from .onedrive import Onedrive

def onedrive_login():
    url = f'{routes.AUTH_URL}?client_id={routes.CLIENT_ID}&scope={routes.SCOPES}&response_type=code&redirect_uri={routes.REDIRECT_URL}'
    webbrowser.open(url)
    server = HTTPServer(('localhost', 8000), OAuth2Handler)
    server.handle_request()
    code = getattr(server, 'code')
    return Onedrive.login(code)