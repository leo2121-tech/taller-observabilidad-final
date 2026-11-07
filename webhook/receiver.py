from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length > 0 else b""

        print(f"[webhook] {self.path}", flush=True)
        try:
            print(raw.decode("utf-8"), flush=True)
        except UnicodeDecodeError:
            print(raw, flush=True)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Webhook receiver running on http://{HOST}:{PORT}", flush=True)
    server.serve_forever()
