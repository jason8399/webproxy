import http.server
from requests import get
import io
import shutil


class WebProxy(http.server.BaseHTTPRequestHandler):
    proxy_url = "http://www.apple.com/"

    def do_GET(self):
        """Serve a GET requests."""
        f = self.get_website()
        if f:
            try:
                shutil.copyfileobj(f, self.wfile)
            finally:
                f.close()

    def get_website(self):
        """Get webview"""
        path = self.proxy_url + self.path[1:]
        respone = get(path)
        self.send_response(respone.status_code)
        f = io.BytesIO()
        f.write(respone.content)
        f.seek(0)
        for title, content in respone.headers.items():
            print(type(title), title)
            if title not in ["Server", "Content-Encoding", "Content-Length",
                             "Date"]:
                self.send_header(title, content)
        self.send_header("Content-Length", str(len(respone.content)))
        self.end_headers()
        return f
