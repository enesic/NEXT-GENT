"""
Interactions API - Vercel Serverless Function
Handles /interactions endpoint for dashboard table
"""
import json
import asyncio
import asyncpg
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"


async def get_interactions(tenant_slug, limit=10, status=None):
    """Get recent interactions for dashboard table"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
        if not tenant:
            await conn.close()
            return []

        tid = tenant['id']

        query = """
            SELECT i.id, i.type, i.summary, i.status, i.created_at,
                   c.first_name, c.last_name, c.customer_id
            FROM interactions i 
            LEFT JOIN customers c ON i.customer_id = c.id
            WHERE i.tenant_id = $1
        """
        params = [tid]
        param_idx = 2

        if status:
            query += f" AND i.status = ${param_idx}"
            params.append(status)
            param_idx += 1

        query += f" ORDER BY i.created_at DESC LIMIT ${param_idx}"
        params.append(min(limit, 20))

        rows = await conn.fetch(query, *params)
        await conn.close()

        interactions = []
        for row in rows:
            first = (row['first_name'] or '').strip()
            last = (row['last_name'] or '').strip()
            name = f"{first} {last}".strip()
            if not name or name.lower() in ('sistem', 'system', 'admin'):
                name = "Müşteri"

            interactions.append({
                "id": row['id'],
                "customer_id": row['customer_id'],
                "customer_name": name,
                "type": row['type'],
                "summary": row['summary'] or "",
                "status": row['status'] or "CONFIRMED",
                "created_at": row['created_at'].isoformat() if row['created_at'] else None
            })

        return interactions
    except Exception as e:
        print(f"Interactions error: {e}")
        return []


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            params = {}
            if "?" in self.path:
                for param in self.path.split("?")[1].split("&"):
                    if "=" in param:
                        k, v = param.split("=", 1)
                        params[k] = v

            tenant = params.get("tenant", "medical")
            limit = min(int(params.get("limit", "10")), 20)
            status = params.get("status")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(get_interactions(tenant, limit, status))
            loop.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.end_headers()
            self.wfile.write(json.dumps(data, default=str).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Tenant-ID")
        self.end_headers()
