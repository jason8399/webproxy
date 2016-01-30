import http.server
from requests import get
import io
import shutil


class WebProxy(http.server.BaseHTTPRequestHandler):
    proxy_url = "http://orange.tw/"
    server_path = "localhost:8000"

    def do_GET(self):
        """Serve a GET requests."""
        f = self.get_website()
        if f:
            try:
                shutil.copyfileobj(f, self.wfile)
            finally:
                f.close()

    def get_website(self):
        """Get WebView"""
        path = self.proxy_url + self.path[1:]
        response = get(path)
        # redirect browser
        if response.history:
            response = response.history.pop()
        self.send_response(response.status_code)
        f = io.BytesIO()
        # Replace all url to proxy path.
        f.write(response.content.replace(bytes(response.url.split("/")[2],
                                               "utf8"),
                                         bytes(self.server_path, "utf8")))
        f.seek(0)
        for title, content in response.headers.items():
            if title.lower() not in ["server", "content-encoding",
                                     "content-length", "date"]:
                if title.lower() in "location":
                    content = content.replace(response.url.split("/")[2],
                                              self.server_path)
                self.send_header(title, content)
        self.send_header("Content-Length", str(len(response.content)))
        self.end_headers()
        return f
