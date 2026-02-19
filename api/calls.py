"""
Calls API - Optimized with pagination and real data
"""
import json
import asyncio
import asyncpg
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters for pagination
            path = self.path
            tenant_slug = "beauty"
            page = 1
            limit = 15  # Reasonable limit
            
            if "?" in path:
                query_params = path.split("?")[1]
                for param in query_params.split("&"):
                    if "tenant=" in param:
                        tenant_slug = param.split("=")[1]
                    elif "page=" in param:
                        page = max(1, int(param.split("=")[1]))
                    elif "limit=" in param:
                        limit = min(int(param.split("=")[1]), 25)  # Max 25

            offset = (page - 1) * limit

            # Run async calls fetch from database
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                calls, total = loop.run_until_complete(self.get_calls(tenant_slug, limit, offset))
            finally:
                loop.close()
            
            response_data = {
                "status": "success",
                "data": calls,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit
                }
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
                "message": f"Calls error: {str(e)}",
                "data": []
            }
            self.wfile.write(json.dumps(error_data).encode())

    async def get_calls(self, tenant_slug: str, limit: int, offset: int):
        """Get paginated real call interactions from database"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get tenant info
            tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
            if not tenant:
                await conn.close()
                return [], 0
            
            # Get real call interactions from database
            calls_data = await conn.fetch("""
                SELECT 
                    ci.id,
                    ci.interaction_type,
                    ci.call_duration_seconds,
                    ci.satisfaction_score,
                    ci.resolution_status,
                    ci.agent_name,
                    ci.call_timestamp,
                    ci.call_summary,
                    c.customer_id,
                    c.first_name,
                    c.last_name,
                    c.phone_hash
                FROM call_interactions ci
                JOIN customers c ON ci.customer_id = c.id
                WHERE ci.tenant_id = $1
                ORDER BY ci.call_timestamp DESC
                LIMIT $2 OFFSET $3
            """, tenant['id'], limit, offset)
            
            # Get total count
            total_count = await conn.fetchval("""
                SELECT COUNT(*) FROM call_interactions 
                WHERE tenant_id = $1
            """, tenant['id'])
            
            # Format calls for frontend
            calls = []
            for call_data in calls_data:
                # Format duration
                duration_minutes = call_data['call_duration_seconds'] // 60
                duration_seconds = call_data['call_duration_seconds'] % 60
                duration_formatted = f"{duration_minutes}m {duration_seconds}s"
                
                # Get masked phone (show only last 4 chars of hash for demo)
                masked_phone = f"****{call_data['phone_hash'][-4:]}" if call_data['phone_hash'] else "****"
                
                # Build clean customer name, skip 'Sistem' variants
                first = (call_data['first_name'] or '').strip()
                last = (call_data['last_name'] or '').strip()
                cust_name = f"{first} {last}".strip()
                if not cust_name or cust_name.lower() in ('sistem', 'system', 'admin'):
                    cust_name = "Müşteri"
                
                call = {
                    "id": call_data['id'],
                    "customer_id": call_data['customer_id'],
                    "customer_name": cust_name,
                    "phone": masked_phone,  # KVKK compliant
                    "type": call_data['interaction_type'],
                    "duration": duration_formatted,
                    "duration_seconds": call_data['call_duration_seconds'],
                    "satisfaction": call_data['satisfaction_score'],
                    "status": call_data['resolution_status'],
                    "agent": call_data['agent_name'],
                    "timestamp": call_data['call_timestamp'].isoformat(),
                    "summary": call_data['call_summary'] or f"{call_data['interaction_type'].title()} call",
                    "tenant_id": tenant['id']
                }
                calls.append(call)
            
            await conn.close()
            return calls, total_count or 0
            
        except Exception as e:
            return [], 0

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()