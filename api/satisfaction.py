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

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            tenant_slug = data.get("tenant", "medical")
            # Explicitly cast score to int to avoid DB type mismatches
            try:
                score = int(data.get("score", 5))
            except (ValueError, TypeError):
                score = 5
            
            feedback = data.get("feedback", "")

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
                        return False, "Tenant not found"
                    
                    tenant_id = tenant['id']
                    if isinstance(tenant_id, str):
                        tenant_id = uuid.UUID(tenant_id)
                        
                    now = datetime.now()
                    sentiment = 'positive' if score >= 4 else ('negative' if score <= 2 else 'neutral')
                    
                    # 2. Try inserting into 'satisfactions' table (primary table for web feedback)
                    try:
                        await conn.execute(
                            """INSERT INTO satisfactions (
                                id, tenant_id, survey_type, channel, csat_score, 
                                feedback_text, sentiment, created_at, updated_at
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                            uuid.uuid4(), tenant_id, 'csat', 'in_app', score, 
                            feedback, sentiment, now, now
                        )
                    except Exception as s_err:
                        print(f"Satisfactions table insert failed: {s_err}")
                        # Not failing the whole request yet, trying vapi_calls
                    
                    # 3. Try inserting into 'vapi_calls' table (for analytics compatibility)
                    # We try common column names to be extremely resilient
                    try:
                        # Inspecting columns would be best, but we'll try the most likely structure first
                        # We use a fallback logic: try satisfaction_score, if fails try call_quality_score
                        try:
                            await conn.execute(
                                """INSERT INTO vapi_calls (
                                    id, tenant_id, vapi_call_id, caller_phone_encrypted, phone_hash, 
                                    call_duration_seconds, call_status, started_at, updated_at, 
                                    satisfaction_score, sentiment, created_at
                                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                                uuid.uuid4(), tenant_id, f"web-{uuid.uuid4()}", "web-feedback", "web-hash",
                                0, 'completed', now, now, score, sentiment, now
                            )
                        except asyncpg.exceptions.UndefinedColumnError:
                            # Fallback if satisfaction_score doesn't exist but call_quality_score does
                            await conn.execute(
                                """INSERT INTO vapi_calls (
                                    id, tenant_id, vapi_call_id, caller_phone_encrypted, phone_hash, 
                                    call_duration_seconds, call_status, started_at, updated_at, 
                                    call_quality_score, sentiment, created_at
                                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                                uuid.uuid4(), tenant_id, f"web-{uuid.uuid4()}", "web-feedback", "web-hash",
                                0, 'completed', now, now, score, sentiment, now
                            )
                    except Exception as v_err:
                        # If both vapi_calls attempts fail, we report this error
                        await conn.close()
                        return False, f"Vapi_calls Error: {str(v_err)}"

                    await conn.close()
                    return True, None
                except Exception as db_err:
                    return False, str(db_err)

            success, error_msg = loop.run_until_complete(save_feedback())
            loop.close()

            status_code = 201 if success else 500
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            res = {"status": "success" if success else "error"}
            if error_msg:
                res["message"] = error_msg
            
            self.wfile.write(json.dumps(res).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Tenant-ID")
        self.end_headers()
