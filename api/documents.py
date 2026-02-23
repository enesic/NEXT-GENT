"""
Documents API - Sectoral documents
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
            # Parse query parameters
            path = self.path
            tenant_slug = "beauty"
            limit = 20  # Default limit for performance
            
            if "?" in path:
                query_params = path.split("?")[1]
                for param in query_params.split("&"):
                    if "tenant=" in param:
                        tenant_slug = param.split("=")[1]
                    elif "limit=" in param:
                        limit = min(int(param.split("=")[1]), 50)  # Max 50 for performance

            # Run async documents fetch
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                documents = loop.run_until_complete(self.get_documents(tenant_slug, limit))
            finally:
                loop.close()
            
            # Return plain array so response.data.map() works in all frontend versions
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(documents).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_data = {
                "status": "error",
                "message": f"Documents error: {str(e)}",
                "data": []  # Return empty array on error
            }
            self.wfile.write(json.dumps(error_data).encode())

    async def get_documents(self, tenant_slug: str, limit: int):
        """Get sectoral documents"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get tenant info
            tenant = await conn.fetchrow("SELECT id, name FROM tenants WHERE slug = $1", tenant_slug)
            if not tenant:
                await conn.close()
                return []
            
            # Generate realistic sectoral documents
            documents = []
            sector_docs = self.get_sector_documents(tenant_slug)
            
            # Generate documents for last 30 days
            base_date = datetime.now()
            doc_id_counter = 1
            
            for i in range(min(limit, 30)):
                doc_date = base_date - timedelta(days=i)
                
                # Add 1-2 documents per day
                import random
                for _ in range(random.randint(1, 2)):
                    if doc_id_counter > limit:
                        break
                        
                    doc_template = random.choice(sector_docs)
                    
                    documents.append({
                        "id": doc_id_counter,
                        "filename": doc_template["title"],
                        "file_type": self.get_mime_from_type(doc_template["type"]),
                        "created_at": doc_date.isoformat(),
                        "updated_at": doc_date.isoformat(),
                        "status": random.choice(["active", "archived", "pending"]),
                        "size": random.randint(51200, 512000),
                        "category": doc_template["category"],
                        "tenant_id": tenant['id'],
                        "file_url": f"/documents/{tenant_slug}/{doc_id_counter}.pdf"
                    })
                    
                    doc_id_counter += 1
                    
                    if doc_id_counter > limit:
                        break
            
            await conn.close()
            return documents
            
        except Exception as e:
            return []

    def get_sector_documents(self, sector: str):
        """Get sector-specific document types"""
        sector_documents = {
            "beauty": [
                {"title": "Müşteri Dosyası", "type": "customer_file", "description": "Müşteri cilt analiz raporu", "category": "customer"},
                {"title": "Randevu Formu", "type": "appointment", "description": "Randevu kayıt formu", "category": "booking"},
                {"title": "Tedavi Planı", "type": "treatment_plan", "description": "Kişisel bakım planı", "category": "treatment"},
                {"title": "Ürün Kataloğu", "type": "catalog", "description": "Kozmetik ürün kataloğu", "category": "product"}
            ],
            "automotive": [
                {"title": "Araç Servisi Raporu", "type": "service_report", "description": "Periyodik bakım raporu", "category": "maintenance"},
                {"title": "Yedek Parça Faturası", "type": "invoice", "description": "Parça değişim faturası", "category": "billing"},
                {"title": "Araç Muayene", "type": "inspection", "description": "Teknik muayene raporu", "category": "inspection"},
                {"title": "Garanti Belgesi", "type": "warranty", "description": "Araç garanti belgesi", "category": "warranty"}
            ],
            "medical": [
                {"title": "Hasta Dosyası", "type": "patient_file", "description": "Hasta kayıt dosyası", "category": "patient"},
                {"title": "Tahlil Sonucu", "type": "test_result", "description": "Laboratuvar test sonuçları", "category": "lab"},
                {"title": "Reçete", "type": "prescription", "description": "İlaç reçetesi", "category": "prescription"},
                {"title": "Muayene Raporu", "type": "examination", "description": "Doktor muayene raporu", "category": "examination"}
            ],
            "finance": [
                {"title": "Kredi Başvurusu", "type": "loan_application", "description": "Kredi başvuru formu", "category": "loan"},
                {"title": "Yatırım Raporu", "type": "investment_report", "description": "Portföy performans raporu", "category": "investment"},
                {"title": "Sigorta Poliçesi", "type": "insurance_policy", "description": "Sigorta poliçe belgesi", "category": "insurance"},
                {"title": "Hesap Özeti", "type": "account_statement", "description": "Aylık hesap özeti", "category": "statement"}
            ]
        }
        
        return sector_documents.get(sector, sector_documents["beauty"])

    def get_mime_from_type(self, doc_type: str) -> str:
        """Map internal doc type to MIME type string for frontend getFileTypeFromMime()"""
        mime_map = {
            "customer_file": "application/pdf",
            "appointment":   "application/pdf",
            "treatment_plan":"application/pdf",
            "catalog":       "application/pdf",
            "service_report":"application/pdf",
            "invoice":       "application/pdf",
            "inspection":    "application/pdf",
            "warranty":      "application/pdf",
            "patient_file":  "application/pdf",
            "test_result":   "application/pdf",
            "prescription":  "application/pdf",
            "examination":   "application/pdf",
            "loan_application":   "application/pdf",
            "investment_report":  "application/pdf",
            "insurance_policy":   "application/pdf",
            "account_statement":  "application/pdf",
        }
        return mime_map.get(doc_type, "application/pdf")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()