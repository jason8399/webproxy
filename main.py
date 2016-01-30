from http.server import HTTPServer
from webproxy import WebProxy
import socketserver


class ThreadedTCPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


def run(server_class=HTTPServer, handler_class=WebProxy):
    server_address = ('', 8000)
    httpd = ThreadedTCPServer(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
