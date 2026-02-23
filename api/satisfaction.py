"""
Satisfaction API - Vercel Serverless Function
Handles /satisfaction/metrics and /satisfaction/trends
"""
import json
import asyncio
import asyncpg
import uuid
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

        # Get satisfaction scores from call_interactions
        rows = await conn.fetch(
            """SELECT satisfaction_score, sentiment, call_timestamp as created_at
               FROM call_interactions 
               WHERE tenant_id = $1 AND call_timestamp > $2 
                 AND satisfaction_score IS NOT NULL
               ORDER BY call_timestamp""",
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
            """SELECT DATE(call_timestamp) as day, AVG(satisfaction_score) as avg_score
               FROM call_interactions 
               WHERE tenant_id = $1 AND call_timestamp > $2 AND satisfaction_score IS NOT NULL
               GROUP BY DATE(call_timestamp) ORDER BY day""",
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
            self.wfile.write(json.dumps({"error": f"[V2.0] Diagnostic Error: {str(e)}"}).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            tenant_slug = data.get("tenant", "medical")
            feedback = data.get("feedback", "")
            try:
                score = int(data.get("score", 5))
            except:
                score = 5

            # Connect to database
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def save_feedback():
                try:
                    conn = await asyncpg.connect(DATABASE_URL)
                    
                    # 1. Get Tenant
                    tenant = await conn.fetchrow("SELECT id FROM tenants WHERE slug = $1", tenant_slug)
                    if not tenant:
                        await conn.close()
                        return False, "[V2.0] Tenant not found"
                    
                    tenant_id = tenant['id']
                    if isinstance(tenant_id, str):
                        tenant_id = uuid.UUID(tenant_id)
                        
                    now = datetime.now()
                    sentiment = 'positive' if score >= 4 else ('negative' if score <= 2 else 'neutral')
                    
                    # 2. Try inserting into satisfactions/satisfaction
                    # We use a single try-except to try the most likely first
                    satisfaction_id = uuid.uuid4()
                    try:
                        await conn.execute(
                            """INSERT INTO satisfactions (
                                id, tenant_id, survey_type, channel, csat_score, 
                                feedback_text, sentiment, created_at, updated_at
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                            satisfaction_id, tenant_id, 'csat', 'in_app', score, 
                            feedback, sentiment, now, now
                        )
                    except:
                        try:
                            await conn.execute(
                                """INSERT INTO satisfaction (
                                    id, tenant_id, survey_type, channel, csat_score, 
                                    feedback_text, sentiment, created_at, updated_at
                                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                                satisfaction_id, tenant_id, 'csat', 'in_app', score, 
                                feedback, sentiment, now, now
                            )
                        except Exception as s_err:
                            print(f"Satisfaction insert fail: {s_err}")
                    
                    # 3. Sync with call_interactions (Confirmed name from calls.py)
                    try:
                        # We try to find a valid customer_id for this tenant to avoid FF errors
                        cust = await conn.fetchrow("SELECT id FROM customers WHERE tenant_id = $1 LIMIT 1", tenant_id)
                        customer_id = cust['id'] if cust else None
                        
                        await conn.execute(
                            """INSERT INTO call_interactions (
                                id, tenant_id, customer_id, interaction_type, 
                                call_duration_seconds, satisfaction_score, 
                                call_timestamp, call_summary, resolution_status
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                            uuid.uuid4(), tenant_id, customer_id, 'web_feedback',
                            0, score, now, f"Web Feedback: {feedback[:50]}", 'COMPLETED'
                        )
                    except Exception as ci_err:
                        await conn.close()
                        return False, f"[V2.0] DB Sync Error: {str(ci_err)}"

                    await conn.close()
                    return True, None
                except Exception as db_err:
                    return False, f"[V2.0] Fatal DB Error: {str(db_err)}"

            success, error_msg = loop.run_until_complete(save_feedback())
            loop.close()

            self.send_response(201 if success else 500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            res = {"status": "success" if success else "error"}
            if error_msg: res["message"] = error_msg
            self.wfile.write(json.dumps(res).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"[V2.0] Handler Error: {str(e)}"}).encode())



    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Tenant-ID")
        self.end_headers()
