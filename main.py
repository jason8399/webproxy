from http.server import HTTPServer, BaseHTTPRequestHandler
from webproxy import WebProxy


def run(server_class=HTTPServer, handler_class=WebProxy):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()