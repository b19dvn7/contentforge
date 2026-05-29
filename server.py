"""Simple web server for ContentForge validation landing page.
Handles static file serving and email signup collection.
Exposed via localtunnel for public access."""

import json
import os
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

SIGNUPS_FILE = Path(__file__).parent / "signups.json"
LANDING_DIR = Path(__file__).parent / "landing"

class ContentForgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "":
            self._serve_file("index.html")
        elif path == "/signups":
            self._serve_signups()
        elif path == "/health":
            self._json_response({"status": "ok"}, 200)
        else:
            self._serve_file(path.lstrip("/"))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/signup":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(body)
            email = params.get("email", [None])[0]
            if email:
                self._save_signup(email)
                self._json_response({"status": "ok", "message": "Signed up!"}, 200)
            else:
                self._json_response({"status": "error", "message": "Email required"}, 400)
        else:
            self._json_response({"status": "error", "message": "Not found"}, 404)

    def _serve_file(self, filename):
        filepath = LANDING_DIR / filename
        if not filepath.exists() or not filepath.is_file():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        ext = filepath.suffix.lower()
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        content_type = content_types.get(ext, "application/octet-stream")

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def _serve_signups(self):
        signups = self._load_signups()
        self._json_response({"count": len(signups), "signups": signups}, 200)

    def _save_signup(self, email):
        signups = self._load_signups()
        signups.append({"email": email, "timestamp": self.date_time_string()})
        with open(SIGNUPS_FILE, "w") as f:
            json.dump(signups, f, indent=2)
        print(f"[SIGNUP] {email}")

    def _load_signups(self):
        if SIGNUPS_FILE.exists():
            with open(SIGNUPS_FILE) as f:
                return json.load(f)
        return []

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]} {args[2]}")


def check_prerequisites():
    if not LANDING_DIR.exists():
        print(f"ERROR: Landing directory not found at {LANDING_DIR}")
        print("Create it with index.html first.")
        sys.exit(1)
    if not (LANDING_DIR / "index.html").exists():
        print(f"ERROR: index.html not found in {LANDING_DIR}")
        sys.exit(1)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    check_prerequisites()

    if SIGNUPS_FILE.exists():
        signups = json.loads(SIGNUPS_FILE.read_text())
        print(f"Loaded {len(signups)} existing signups")

    port = int(os.environ.get("PORT", 8080))
    server = ThreadedHTTPServer(("0.0.0.0", port), ContentForgeHandler)
    print(f"\n{'='*60}")
    print(f"ContentForge Validation Server")
    print(f"{'='*60}")
    print(f"Local URL:      http://localhost:{port}")
    print(f"Dashboard:      http://localhost:{port}/signups")
    print(f"Health check:   http://localhost:{port}/health")
    print(f"\nTo expose publicly, run in another terminal:")
    print(f"  lt --port {port} --subdomain contentforge")
    print(f"{'='*60}\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
