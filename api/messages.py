"""
Messages API - Returns empty messages (no system spam)
"""
import json
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Return empty messages - no synthetic spam"""
        page = 1
        limit = 10

        if "?" in self.path:
            for param in self.path.split("?")[1].split("&"):
                if "page=" in param:
                    try:
                        page = max(1, int(param.split("=")[1]))
                    except ValueError:
                        pass
                elif "limit=" in param:
                    try:
                        limit = min(int(param.split("=")[1]), 20)
                    except ValueError:
                        pass

        response_data = {
            "status": "success",
            "data": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "pages": 0
            }
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()