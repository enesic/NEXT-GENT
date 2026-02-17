"""
Vercel Serverless Function for Tenant Info  
Endpoint: /api/v1/tenants/me
"""
import os
import json
import asyncio
import asyncpg
from http.server import BaseHTTPRequestHandler

# Set environment variables
os.environ["ENVIRONMENT"] = "production"
os.environ["DEBUG"] = "false"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["ENCRYPTION_KEY"] = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="
os.environ["BACKEND_CORS_ORIGINS"] = "https://www.nextgent.co,https://nextgent.co,http://localhost:5173"
os.environ["REDIS_HOST"] = ""

async def get_tenant_info():
    """Get default tenant information"""
    try:
        conn = await asyncpg.connect(os.environ["DATABASE_URL"])
        
        # Get default tenant (nextgent-main)
        tenant = await conn.fetchrow("""
            SELECT id, name, slug, domain, config, webhook_url, system_prompt, is_active
            FROM tenants 
            WHERE slug = 'nextgent-main' AND is_active = true
        """)
        
        await conn.close()
        
        if tenant:
            return {
                "id": tenant['id'],
                "name": tenant['name'],
                "slug": tenant['slug'],
                "domain": tenant['domain'],
                "config": tenant['config'] or {"sector": "beauty"},
                "webhook_url": tenant['webhook_url'],
                "system_prompt": tenant['system_prompt'],
                "is_active": tenant['is_active']
            }
        else:
            # Return default if not found
            return {
                "id": 1,
                "name": "NextGent Main",
                "slug": "nextgent-main", 
                "domain": "nextgent.co",
                "config": {"sector": "beauty"},
                "webhook_url": None,
                "system_prompt": None,
                "is_active": True
            }
            
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback tenant info
        return {
            "id": 1,
            "name": "NextGent Main",
            "slug": "nextgent-main",
            "domain": "nextgent.co", 
            "config": {"sector": "beauty"},
            "webhook_url": None,
            "system_prompt": None,
            "is_active": True
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Run async tenant fetch
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tenant_info = loop.run_until_complete(get_tenant_info())
            loop.close()
            
            response_data = {
                "status": "success",
                "data": tenant_info
            }
            
            self.send_response(200)
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
                "message": f"Failed to get tenant info: {str(e)}"
            }
            self.wfile.write(json.dumps(error_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()