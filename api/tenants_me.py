"""
Tenant Info endpoint
"""
import json
import asyncio
import asyncpg
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Run async tenant fetch
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                tenant_info = loop.run_until_complete(self.get_tenant_info())
            finally:
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

    async def get_tenant_info(self):
        """Get tenant information based on domain or default"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get beauty sector as default (most complete)
            tenant = await conn.fetchrow("""
                SELECT id, name, slug, domain, config, webhook_url, system_prompt, is_active
                FROM tenants 
                WHERE slug = 'beauty' AND is_active = true
            """)
            
            await conn.close()
            
            if tenant:
                return {
                    "id": tenant['id'],
                    "name": tenant['name'],
                    "slug": tenant['slug'],
                    "domain": tenant['domain'] or "nextgent.co",
                    "config": json.loads(tenant['config']) if tenant['config'] else {"sector": "beauty"},
                    "webhook_url": tenant['webhook_url'],
                    "system_prompt": tenant['system_prompt'],
                    "is_active": tenant['is_active']
                }
            else:
                # Return fallback
                return {
                    "id": 1,
                    "name": "NextGent Beauty",
                    "slug": "beauty",
                    "domain": "nextgent.co",
                    "config": {"sector": "beauty"},
                    "webhook_url": None,
                    "system_prompt": None,
                    "is_active": True
                }
                
        except Exception as e:
            # Fallback tenant info
            return {
                "id": 1,
                "name": "NextGent Beauty",
                "slug": "beauty",
                "domain": "nextgent.co", 
                "config": {"sector": "beauty"},
                "webhook_url": None,
                "system_prompt": None,
                "is_active": True
            }

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()