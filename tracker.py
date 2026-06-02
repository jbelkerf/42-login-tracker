#!/usr/bin/env python3
"""
42 Login Tracker - Local Script
Automatically opens your browser for 42 OAuth — no copy-pasting needed.
"""

from time import sleep
from requests import get
import subprocess
import threading
import webbrowser
import platform
import socket
import json
import sys
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode

API_BASE  = "https://api.intra.42.fr/v2"
AUTH_SITE = "https://42-tracker-web.vercel.app"

# ── Notification ───────────────────────────────────────────────────────────────

def notify(title, message):
    system = platform.system()
    if system == "Darwin":
        try:
            import pync
            pync.notify(message, title=title)
            return
        except ImportError:
            pass
        subprocess.run(["osascript", "-e",
            f'display notification "{message}" with title "{title}"'])
    else:
        subprocess.run(["notify-send", title, message])

# ── API helpers ────────────────────────────────────────────────────────────────

def fetch_location(token, login):
    resp = get(f"{API_BASE}/users/{login}",
               headers={"Authorization": f"Bearer {token}"})
    if resp.status_code == 401:
        print("\n\033[31m[!] Token expired. Re-run the script to get a new one.\033[0m\n")
        sys.exit(1)
    if resp.status_code == 404:
        print(f"\033[31m[!] User '{login}' not found on 42 intra.\033[0m")
        sys.exit(1)
    if resp.status_code != 200:
        print(f"\033[33m[!] API error {resp.status_code}, retrying...\033[0m")
        return "ERROR"
    return resp.json().get("location")

# ── Tracking ───────────────────────────────────────────────────────────────────

def check_logged(token, user):
    print(f"\033[32m[*] Waiting for \033[1m{user}\033[0m\033[32m to log in...\033[0m  (Ctrl+C to stop)\n")
    while True:
        loc = fetch_location(token, user)
        if loc and loc != "ERROR":
            notify("42 Tracker", f"{user} just logged in at {loc}!")
            print(f"\033[32m[+] {user} logged in at {loc}!\033[0m")
            break
        elif loc != "ERROR":
            print(f"    not logged in yet...", end="\r")
        sleep(10)


def check_delogged(token, user):
    print(f"\033[32m[*] Waiting for \033[1m{user}\033[0m\033[32m to log out...\033[0m  (Ctrl+C to stop)\n")
    while True:
        loc = fetch_location(token, user)
        if loc is None:
            notify("42 Tracker", f"{user} just logged out!")
            print(f"\033[32m[+] {user} logged out!\033[0m")
            break
        elif loc != "ERROR":
            print(f"    still logged in at {loc}...", end="\r")
        sleep(10)

# ── Local OAuth callback server ────────────────────────────────────────────────

def get_free_port():
    """Pick a random free TCP port."""
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def get_token_via_browser():
    """
    Start a one-shot local HTTP server, open the browser to the web app,
    and wait for the OAuth redirect back with the token.
    Returns (token, login_name).
    """
    port   = get_free_port()
    result = {}   # filled in by the handler

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):   # silence access logs
            pass

        def do_GET(self):
            qs = parse_qs(urlparse(self.path).query)
            token      = qs.get("token",  [None])[0]
            login_name = qs.get("login",  ["unknown"])[0]

            if token:
                result["token"]      = token
                result["login_name"] = login_name
                body = (
                    b"<html><body style='font-family:sans-serif;background:#0f0f0f;"
                    b"color:#eee;display:flex;align-items:center;justify-content:center;"
                    b"min-height:100vh;margin:0;text-align:center'>"
                    b"<div><div style='font-size:3rem'>&#10003;</div>"
                    b"<h2>Authenticated!</h2>"
                    b"<p style='color:#aaa'>You can close this tab.</p></div></body></html>"
                )
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing token.")

            # Shut down the server after one request
            threading.Thread(target=self.server.shutdown, daemon=True).start()

    server = HTTPServer(("localhost", port), Handler)

    callback_url = f"http://localhost:{port}"
    login_url    = f"{AUTH_SITE}/login?" + urlencode({"callback": callback_url})

    print(f"\033[36m  Opening browser for authentication...\033[0m")
    print(f"  (If it doesn't open, visit: \033[4m{login_url}\033[0m)\n")
    webbrowser.open(login_url)

    server.serve_forever()   # blocks until handler calls shutdown()

    if "token" not in result:
        print("\033[31m[!] Authentication failed or was cancelled.\033[0m")
        sys.exit(1)

    return result["token"], result["login_name"]

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("logged", "delogged"):
        print("\033[31musage: ./launch.sh <user_to_track> <logged|delogged>\033[0m")
        sys.exit(1)

    user_to_track = sys.argv[1]
    mode          = sys.argv[2]

    print(f"\033[36m")
    print(f"  42 Login Tracker")
    print(f"  ─────────────────────────────────────")
    print(f"\033[0m")

    token, me = get_token_via_browser()

    print(f"\033[32m  [✓] Authenticated as: \033[1m{me}\033[0m\n")

    if mode == "logged":
        check_logged(token, user_to_track)
    else:
        check_delogged(token, user_to_track)


if __name__ == "__main__":
    main()
