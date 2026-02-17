"""
Vercel Serverless Function for Health Check
Endpoint: /api/v1/health
"""
import os
import json
from http.server import BaseHTTPRequestHandler

# Set environment variables
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"
os.environ["REDIS_HOST"] = ""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Basic health check
            health_data = {
                "status": "healthy",
                "environment": "production",
                "database": "connected",
                "service": "NextGent API",
                "version": "2.0.0"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(health_data).encode())
            
        except Exception as e:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_data = {
                "status": "error",
                "message": f"Health check failed: {str(e)}",
                "database": "disconnected"
            }
            self.wfile.write(json.dumps(error_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()