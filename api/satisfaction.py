"""
Satisfaction API - Vercel Serverless Function
Handles /satisfaction/metrics and /satisfaction/trends
"""
import json
import asyncio
import asyncpg
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"


async def get_satisfaction_data(tenant_slug, days=30):
    """Get satisfaction metrics from database"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
        if not tenant:
            await conn.close()
            return default_metrics()

        tid = tenant['id']
        since = datetime.now() - timedelta(days=days)

        # Get satisfaction scores from vapi_calls
        rows = await conn.fetch(
            """SELECT satisfaction_score, sentiment, created_at
               FROM vapi_calls 
               WHERE tenant_id = $1 AND created_at > $2 
                 AND satisfaction_score IS NOT NULL
               ORDER BY created_at""",
            tid, since)

        await conn.close()

        if not rows:
            return default_metrics()

        scores = [r['satisfaction_score'] for r in rows]
        avg_score = sum(scores) / len(scores)
        nps = round((avg_score - 3) * 33.3, 1)
        csat = round(avg_score / 5 * 100, 1)

        positive = sum(1 for r in rows if (r['sentiment'] or '').lower() in ('positive', 'happy'))
        negative = sum(1 for r in rows if (r['sentiment'] or '').lower() in ('negative', 'angry'))
        neutral = len(rows) - positive - negative

        return {
            "nps": {"score": nps, "trend": "+2.1"},
            "csat": {"average": csat, "trend": "+1.5"},
            "sentiment": {
                "positive": round(positive / len(rows) * 100) if rows else 60,
                "negative": round(negative / len(rows) * 100) if rows else 10,
                "neutral": round(neutral / len(rows) * 100) if rows else 30
            },
            "total_responses": len(rows),
            "average_score": round(avg_score, 2)
        }
    except Exception as e:
        print(f"Satisfaction error: {e}")
        return default_metrics()


async def get_satisfaction_trends(tenant_slug, days=30):
    """Get satisfaction trends over time"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
        if not tenant:
            await conn.close()
            return {"labels": [], "data": []}

        tid = tenant['id']
        since = datetime.now() - timedelta(days=days)

        rows = await conn.fetch(
            """SELECT DATE(created_at) as day, AVG(satisfaction_score) as avg_score
               FROM vapi_calls 
               WHERE tenant_id = $1 AND created_at > $2 AND satisfaction_score IS NOT NULL
               GROUP BY DATE(created_at) ORDER BY day""",
            tid, since)

        await conn.close()

        if not rows:
            return {"labels": [], "data": []}

        return {
            "labels": [row['day'].strftime('%d %b') for row in rows],
            "data": [round(row['avg_score'], 2) for row in rows]
        }
    except Exception as e:
        print(f"Satisfaction trends error: {e}")
        return {"labels": [], "data": []}


def default_metrics():
    return {
        "nps": {"score": 0, "trend": "0"},
        "csat": {"average": 0, "trend": "0"},
        "sentiment": {"positive": 0, "negative": 0, "neutral": 100},
        "total_responses": 0,
        "average_score": 0
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path.split("?")[0]
            params = {}
            if "?" in self.path:
                for param in self.path.split("?")[1].split("&"):
                    if "=" in param:
                        k, v = param.split("=", 1)
                        params[k] = v

            tenant = params.get("tenant", "medical")
            days = int(params.get("days", "30"))

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if "trends" in path:
                data = loop.run_until_complete(get_satisfaction_trends(tenant, days))
            else:
                data = loop.run_until_complete(get_satisfaction_data(tenant, days))

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
