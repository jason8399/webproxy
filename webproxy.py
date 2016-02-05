import http.server
from requests import get, post
import io
import shutil
import cgi
from urllib import parse


class WebProxy(http.server.BaseHTTPRequestHandler):
    proxy_url = "https://stucis.ttu.edu.tw/"
    server_path = "localhost:8000"
    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        """Serve a GET requests."""
        f = self.get_website()
        if f:
            try:
                shutil.copyfileobj(f, self.wfile)
            finally:
                f.close()

    def do_POST(self):
        """Serve a POST requests."""

        headers = {}
        for field, value in self.headers.items():
            if field.lower() in ["host", "origin", "referer"]:
                value = value.replace("http://" + self.server_path, self.proxy_url[:-1])
            headers.update({field: value})

        response = post(self.proxy_url + self.path[1:], data=self.rfile.read(len(self.rfile.peek())), headers=headers, verify=False)
        f = self.get_website(response)
        if f:
            try:
                shutil.copyfileobj(f, self.wfile)
            finally:
                f.close()

    def get_website(self, response=None):
        """Get WebView"""
        path = self.proxy_url + self.path[1:]
        if not response:
            headers = {}
            for field, value in self.headers.items():
                if field.lower() in ["host", "origin", "referer"]:
                    value = value.replace("http://" + self.server_path, self.proxy_url[:-1])
                headers.update({field: value})
            response = get(path, headers=headers, verify=False)
        # redirect browser
        if response.history:
            response = response.history.pop()
        self.send_response(response.status_code)
        f = io.BytesIO()
        # Replace all url to proxy path.
        f.write(response.content.replace(bytes(response.url.split("/")[2],
                                               "utf8"),
                                         bytes(self.server_path, "utf8")).
                replace(b"https", b"http"))
        f.seek(0)
        for title, content in response.headers.items():
            if title.lower() not in ["server", "content-encoding",
                                     "content-length", "date"]:
                if title.lower() in "location":
                    content = content.replace(response.url.split("/")[2],
                                              self.server_path)\
                        .replace("https", "http")
                self.send_header(title, content)
        self.send_header("Content-Length", str(len(response.content)))
        self.end_headers()
        return f
