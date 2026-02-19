"""
Messages API - Optimized with pagination
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
            limit = 10  # Reduced for performance
            
            if "?" in path:
                query_params = path.split("?")[1]
                for param in query_params.split("&"):
                    if "tenant=" in param:
                        tenant_slug = param.split("=")[1]
                    elif "page=" in param:
                        page = max(1, int(param.split("=")[1]))
                    elif "limit=" in param:
                        limit = min(int(param.split("=")[1]), 20)  # Max 20 for performance

            offset = (page - 1) * limit

            # Run async messages fetch
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                messages, total = loop.run_until_complete(self.get_messages(tenant_slug, limit, offset))
            finally:
                loop.close()
            
            response_data = {
                "status": "success",
                "data": messages,
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
                "message": f"Messages error: {str(e)}",
                "data": []
            }
            self.wfile.write(json.dumps(error_data).encode())

    async def get_messages(self, tenant_slug: str, limit: int, offset: int):
        """Get paginated sectoral messages"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get tenant info
            tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
            if not tenant:
                await conn.close()
                return [], 0
            
            # Get real customers for this tenant - exclude system/admin accounts
            customers = await conn.fetch(
                """SELECT id, customer_id, first_name, last_name 
                   FROM customers 
                   WHERE tenant_id = $1 
                     AND LOWER(first_name) NOT IN ('sistem', 'system', 'admin', 'test')
                     AND first_name IS NOT NULL 
                     AND first_name != ''
                   LIMIT 20""", 
                tenant['id']
            )
            
            if not customers:
                # Fallback: get any customers if all were filtered
                customers = await conn.fetch(
                    "SELECT id, customer_id, first_name, last_name FROM customers WHERE tenant_id = $1 LIMIT 5", 
                    tenant['id']
                )
            
            if not customers:
                await conn.close()
                return [], 0
            
            # Generate realistic sectoral messages with deterministic pagination
            sector_messages = self.get_sector_messages(tenant_slug)
            
            base_date = datetime.now()
            total_messages = min(len(customers) * len(sector_messages), 20)  # Dynamic total, max 20
            
            import random
            # Use tenant ID as seed for consistency
            random.seed(tenant['id'] * 1000)
            
            # Generate messages with consistent IDs
            all_messages = []
            for i in range(total_messages):
                # Skip items before offset (for pagination)
                if i < offset:
                    continue
                
                # Stop when we have enough for this page
                if len(all_messages) >= limit:
                    break
                
                customer = customers[i % len(customers)]  # Rotate through customers
                message_template = sector_messages[i % len(sector_messages)]  # Rotate through messages
                message_date = base_date - timedelta(hours=i * 3)  # Spread over time
                
                # Build clean customer name, skip 'Sistem' variants
                first = (customer['first_name'] or '').strip()
                last = (customer['last_name'] or '').strip()
                cust_name = f"{first} {last}".strip()
                if not cust_name or cust_name.lower() in ('sistem', 'system', 'admin'):
                    cust_name = "Müşteri"
                
                message = {
                    "id": i + 1,  # Consistent ID
                    "customer_id": customer['customer_id'],
                    "customer_name": cust_name,
                    "message": message_template["message"],
                    "type": message_template["type"],
                    "priority": message_template["priority"],
                    "status": ["read", "unread", "replied"][i % 3],  # Deterministic status
                    "created_at": message_date.isoformat(),
                    "channel": ["whatsapp", "phone", "email", "web"][i % 4],  # Deterministic channel
                    "tenant_id": tenant['id']
                }
                
                all_messages.append(message)
            
            await conn.close()
            return all_messages, total_messages
            
        except Exception as e:
            return [], 0

    def get_sector_messages(self, sector: str):
        """Get sector-specific message templates"""
        sector_messages = {
            "beauty": [
                {"message": "Randevumu değiştirmek istiyorum.", "type": "appointment", "priority": "medium"},
                {"message": "Kullandığım ürün hakkında bilgi alabilir miyim?", "type": "product_inquiry", "priority": "low"},
                {"message": "Cilt bakım tedavim ne zaman başlayacak?", "type": "treatment", "priority": "high"},
                {"message": "Fiyat listesini gönderebilir misiniz?", "type": "pricing", "priority": "medium"}
            ],
            "automotive": [
                {"message": "Aracımın servisi ne zaman bitecek?", "type": "service_inquiry", "priority": "high"},
                {"message": "Yedek parça garantisi var mı?", "type": "warranty", "priority": "medium"},
                {"message": "Randevu alabilir miyim?", "type": "appointment", "priority": "medium"},
                {"message": "Fatura detaylarını görüntüleyebilir miyim?", "type": "billing", "priority": "low"}
            ],
            "medical": [
                {"message": "Tahlil sonuçlarım hazır mı?", "type": "test_result", "priority": "high"},
                {"message": "Doktor randevusu alabilir miyim?", "type": "appointment", "priority": "medium"},
                {"message": "İlaç dozu hakkında bilgi alabilir miyim?", "type": "prescription", "priority": "high"},
                {"message": "Muayene ücretini nasıl ödeyebilirim?", "type": "payment", "priority": "low"}
            ],
            "finance": [
                {"message": "Kredi başvurum onaylandı mı?", "type": "loan_status", "priority": "high"},
                {"message": "Hesap bakiyem ne kadar?", "type": "balance_inquiry", "priority": "medium"},
                {"message": "Yatırım önerileriniz var mı?", "type": "investment_advice", "priority": "low"},
                {"message": "Kart bloke işlemini nasıl yapabilirim?", "type": "card_issue", "priority": "high"}
            ]
        }
        
        return sector_messages.get(sector, sector_messages["beauty"])

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()