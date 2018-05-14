from http.server import HTTPServer, BaseHTTPRequestHandler


class TestHandler(BaseHTTPRequestHandler):

    def _print_request_data(self):
        content_length = self.headers['Content-Length']
        print("Content-length: {}".format(content_length))
        data = self.rfile.read(int(content_length))
        print(data.decode('utf-8'))

    def _send_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self, *args, **kwargs):
        print('POST request received')
        self._print_request_data()
        self._send_200()

    def do_PUT(self, *args, **kwargs):
        print("PUT request received")
        self._print_request_data()
        self._send_200()


def run(server_class=HTTPServer, handler_class=TestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
