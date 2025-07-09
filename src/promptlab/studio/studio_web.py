import http
from importlib.resources import files


class StudioWebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (
            self.path == "/"
            or self.path.startswith("/datasets")
            or self.path.startswith("/prompts")
        ):
            self._serve_index_html()
        else:
            super().do_GET()

    def _serve_index_html(self):
        try:
            web_files = files("web")
            index_file = web_files / "index.html"
            with index_file.open("rb") as f:
                file_content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(file_content)

        except Exception as e:
            # If resource loading fails, send a 404
            self.send_error(404, f"Could not load index.html: {e}")
