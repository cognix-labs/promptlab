import http
import pkg_resources


class StudioWebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = pkg_resources.resource_filename("web", "index.html")
            with open(self.path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        else:
            super().do_GET()
