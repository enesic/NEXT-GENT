"""
Auth Login endpoint for NextGent - All Sectors
"""
import os
import json
import asyncio
import asyncpg
import bcrypt
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data) if post_data else {}
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_data = {"status": "error", "message": "Invalid JSON"}
                self.wfile.write(json.dumps(error_data).encode())
                return
            
            customer_id = data.get('customer_id', '').strip()
            pin = data.get('pin', '').strip()
            
            if not customer_id or not pin:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_data = {
                    "status": "error",
                    "message": "Missing customer_id or pin"
                }
                self.wfile.write(json.dumps(error_data).encode())
                return
            
            # Run async authentication
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                customer_data, token = loop.run_until_complete(self.authenticate_customer(customer_id, pin))
                
                if customer_data:
                    response_data = {
                        "status": "success",
                        "message": "Login successful",
                        "token": token,
                        "customer": customer_data
                    }
                    self.send_response(200)
                else:
                    response_data = {
                        "status": "error", 
                        "message": token  # error message
                    }
                    self.send_response(401)
                    
            finally:
                loop.close()
            
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
    
    async def authenticate_customer(self, customer_id: str, pin: str):
        """Authenticate customer against Neon database"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get customer with tenant info
            customer = await conn.fetchrow("""
                SELECT c.id, c.customer_id, c.first_name, c.last_name, c.email, 
                       c.pin_hash, c.segment, c.status, c.tenant_id,
                       t.slug as tenant_slug, t.name as tenant_name, t.config as tenant_config
                FROM customers c
                JOIN tenants t ON c.tenant_id = t.id
                WHERE c.customer_id = $1 AND c.status = 'active'
            """, customer_id)
            
            if not customer:
                await conn.close()
                return None, "Customer not found or inactive"
            
            # Verify PIN
            if not bcrypt.checkpw(pin.encode('utf-8'), customer['pin_hash'].encode('utf-8')):
                await conn.close()
                return None, "Invalid PIN"
            
            # Generate simple token
            token = f"customer_{customer['id']}_{customer_id}"
            
            customer_data = {
                "id": customer['customer_id'],
                "name": f"{customer['first_name']} {customer['last_name']}",
                "email": customer['email'],
                "segment": customer['segment'],
                "tenant_id": customer['tenant_id'],
                "tenant_slug": customer['tenant_slug'],
                "tenant_name": customer['tenant_name'],
                "tenant_config": customer['tenant_config']
            }
            
            await conn.close()
            return customer_data, token
            
        except Exception as e:
            return None, f"Database error: {str(e)}"

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()