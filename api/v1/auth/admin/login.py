"""
Vercel Serverless Function for Admin Login
Endpoint: /api/v1/auth/admin/login
"""
import os
import json
import asyncio
import asyncpg
import bcrypt
from http.server import BaseHTTPRequestHandler

# Set environment variables
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"
os.environ["REDIS_HOST"] = ""

async def authenticate_admin(username: str, password: str):
    """Authenticate admin against Neon database"""
    try:
        conn = await asyncpg.connect(os.environ["DATABASE_URL"])
        
        # Get admin user
        admin = await conn.fetchrow("""
            SELECT id, username, email, password_hash, role, is_active, 
                   is_super_admin, permissions, login_count
            FROM admin_users
            WHERE username = $1 AND is_active = true
        """, username)
        
        if not admin:
            await conn.close()
            return None, "Admin user not found or inactive"
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'].encode('utf-8')):
            await conn.close()
            return None, "Invalid password"
        
        # Update login count and last login
        await conn.execute("""
            UPDATE admin_users 
            SET login_count = login_count + 1, last_login_at = NOW()
            WHERE id = $1
        """, admin['id'])
        
        # Generate simple token
        token = f"admin_{admin['id']}_{username}"
        
        admin_data = {
            "id": admin['id'],
            "username": admin['username'],
            "email": admin['email'],
            "role": admin['role'],
            "is_super_admin": admin['is_super_admin'],
            "permissions": admin['permissions'] or {},
            "login_count": admin['login_count'] + 1
        }
        
        await conn.close()
        return admin_data, token
        
    except Exception as e:
        print(f"Database error: {e}")
        return None, f"Database error: {str(e)}"

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
            
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_data = {
                    "status": "error",
                    "message": "Missing username or password"
                }
                self.wfile.write(json.dumps(error_data).encode())
                return
            
            # Run async authentication
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            admin, result = loop.run_until_complete(authenticate_admin(username, password))
            loop.close()
            
            if admin:
                response_data = {
                    "status": "success",
                    "message": "Admin login successful",
                    "token": result,
                    "admin": admin
                }
                self.send_response(200)
            else:
                response_data = {
                    "status": "error",
                    "message": result
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
                "message": f"Admin login failed: {str(e)}"
            }
            self.wfile.write(json.dumps(error_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()