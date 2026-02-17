"""
Vercel Serverless Function for Auth Login
Endpoint: /api/v1/auth/login
"""
import os
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Add api directory to Python path
api_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(api_path))

# Set environment variables
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"
os.environ["REDIS_HOST"] = ""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data) if post_data else {}
            except json.JSONDecodeError:
                data = {}
            
            # Simple demo response for now
            customer_id = data.get('customer_id', '')
            pin = data.get('pin', '')
            
            # Demo credentials: BEA-000001 / 1234
            if customer_id == 'BEA-000001' and pin == '1234':
                response_data = {
                    "status": "success",
                    "message": "Login successful",
                    "token": "demo-token-12345",
                    "customer": {
                        "id": "BEA-000001",
                        "name": "NextGent Demo",
                        "segment": "regular"
                    }
                }
                self.send_response(200)
            else:
                response_data = {
                    "status": "error",
                    "message": "Invalid credentials",
                    "details": "Customer ID or PIN is incorrect"
                }
                self.send_response(401)
            
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_data = {
                "status": "error",
                "message": f"Login failed: {str(e)}"
            }
            self.wfile.write(json.dumps(error_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()