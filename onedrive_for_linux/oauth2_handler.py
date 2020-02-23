import re
import json
from http.server import BaseHTTPRequestHandler

class OAuth2Handler(BaseHTTPRequestHandler):

    success_message = """
        <!DOCTYPE html>
        <head>
            <meta charset="utf-8">
            <title>OneDrive for Linux</title>
            </head>
        <body>
            <p id="token">
            <script>
                var url = new URL(window.location.href);
                var code = url.searchParams.get("code");
                token = document.querySelector("#token");
                token.textContent = "O access_token é: " + code;
            </script>
        </body>
        </html>
    """

    error_message = """
        <!DOCTYPE html>
        <head>
            <meta charset="utf-8">
            <title>OneDrive for Linux</title>
        </head>
        <body>
            <p> Houve um erro ao obter o código de acesso</p>
        </body>
        </html>
    """

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        exp = re.search(r'[?&]code=([^&]+).*$', self.path)
        if (exp != None):
            self.server.code = exp.group().split('=')[1]
            self.wfile.write(OAuth2Handler.success_message.encode())
        else:
            self.wfile.write(OAuth2Handler.error_message.encode())

    def log_message(self, format, *args):
        return
