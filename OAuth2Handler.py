import re
from http.server import BaseHTTPRequestHandler

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