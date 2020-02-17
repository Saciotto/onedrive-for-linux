from OAuth2Handler import OAuth2Handler
from http.server import HTTPServer
import webbrowser

url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=c22bd74f-da4c-460d-af0a-f97aa232a908&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=http://localhost:8000"
webbrowser.open(url)

httpd = HTTPServer(('localhost', 8000), OAuth2Handler)
httpd.handle_request()

print(httpd.access_token)