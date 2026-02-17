"""
Dashboard Configuration API - Sectoral customization
"""
import json
import asyncio
import asyncpg
from http.server import BaseHTTPRequestHandler

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            path = self.path
            tenant_slug = "beauty"
            
            if "?" in path:
                query_params = path.split("?")[1]
                for param in query_params.split("&"):
                    if "tenant=" in param:
                        tenant_slug = param.split("=")[1]

            # Run async dashboard config fetch
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                config = loop.run_until_complete(self.get_dashboard_config(tenant_slug))
            finally:
                loop.close()
            
            response_data = {
                "status": "success",
                "data": config
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
                "message": f"Dashboard config error: {str(e)}",
                "data": {}
            }
            self.wfile.write(json.dumps(error_data).encode())

    async def get_dashboard_config(self, tenant_slug: str):
        """Get sectoral dashboard configuration"""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Get tenant info
            tenant = await conn.fetchrow("SELECT id, name, config FROM tenants WHERE slug = $1", tenant_slug)
            
            await conn.close()
            
            # Return sector-specific dashboard config
            return self.get_sector_dashboard_config(tenant_slug, tenant)
            
        except Exception as e:
            return self.get_sector_dashboard_config(tenant_slug, None)

    def get_sector_dashboard_config(self, sector: str, tenant_data):
        """Get sector-specific dashboard configurations"""
        
        base_config = {
            "theme": {
                "primary_color": "#6366f1",
                "accent_color": "#8b5cf6",
                "background": "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
            },
            "tenant": {
                "id": tenant_data['id'] if tenant_data else 1,
                "name": tenant_data['name'] if tenant_data else "NextGent",
                "slug": sector
            }
        }
        
        sector_configs = {
            "beauty": {
                **base_config,
                "title": "Güzellik & Estetik Dashboard",
                "theme": {
                    "primary_color": "#ec4899",
                    "accent_color": "#f97316", 
                    "background": "bg-gradient-to-br from-pink-900 via-purple-800 to-indigo-900"
                },
                "widgets": [
                    {"id": "appointments", "title": "Günlük Randevular", "icon": "calendar", "priority": 1},
                    {"id": "treatments", "title": "Aktif Tedaviler", "icon": "sparkles", "priority": 2},
                    {"id": "customer_satisfaction", "title": "Müşteri Memnuniyeti", "icon": "star", "priority": 3},
                    {"id": "revenue", "title": "Günlük Gelir", "icon": "dollar-sign", "priority": 4}
                ],
                "kpis": {
                    "daily_appointments": "Günlük Randevu",
                    "treatment_completion": "Tedavi Tamamlanma",
                    "product_sales": "Ürün Satış",
                    "customer_retention": "Müşteri Bağlılığı"
                }
            },
            "automotive": {
                **base_config,
                "title": "Otomotiv Servisi Dashboard",
                "theme": {
                    "primary_color": "#0ea5e9",
                    "accent_color": "#06b6d4",
                    "background": "bg-gradient-to-br from-blue-900 via-slate-800 to-gray-900"
                },
                "widgets": [
                    {"id": "vehicle_services", "title": "Araç Servis", "icon": "wrench", "priority": 1},
                    {"id": "parts_inventory", "title": "Parça Stoku", "icon": "package", "priority": 2},
                    {"id": "service_quality", "title": "Servis Kalitesi", "icon": "shield-check", "priority": 3},
                    {"id": "daily_revenue", "title": "Günlük Ciro", "icon": "trending-up", "priority": 4}
                ],
                "kpis": {
                    "vehicles_serviced": "Servis Edilen Araç",
                    "parts_sold": "Satılan Parça",
                    "service_time": "Ortalama Servis Süresi",
                    "customer_satisfaction": "Müşteri Memnuniyeti"
                }
            },
            "medical": {
                **base_config,
                "title": "Sağlık Merkezi Dashboard",
                "theme": {
                    "primary_color": "#10b981",
                    "accent_color": "#06d6a0",
                    "background": "bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900"
                },
                "widgets": [
                    {"id": "patient_appointments", "title": "Hasta Randevuları", "icon": "user-check", "priority": 1},
                    {"id": "lab_results", "title": "Tahlil Sonuçları", "icon": "activity", "priority": 2},
                    {"id": "treatment_progress", "title": "Tedavi İlerlemesi", "icon": "trending-up", "priority": 3},
                    {"id": "patient_satisfaction", "title": "Hasta Memnuniyeti", "icon": "heart", "priority": 4}
                ],
                "kpis": {
                    "daily_patients": "Günlük Hasta",
                    "lab_tests": "Laboratuvar Test",
                    "prescription_count": "Reçete Sayısı",
                    "treatment_success": "Tedavi Başarı Oranı"
                }
            },
            "finance": {
                **base_config,
                "title": "Finans & Bankacılık Dashboard",
                "theme": {
                    "primary_color": "#f59e0b",
                    "accent_color": "#d97706",
                    "background": "bg-gradient-to-br from-amber-900 via-orange-800 to-red-900"
                },
                "widgets": [
                    {"id": "loan_applications", "title": "Kredi Başvuruları", "icon": "credit-card", "priority": 1},
                    {"id": "investment_portfolio", "title": "Yatırım Portföyü", "icon": "trending-up", "priority": 2},
                    {"id": "customer_accounts", "title": "Müşteri Hesapları", "icon": "users", "priority": 3},
                    {"id": "daily_transactions", "title": "Günlük İşlemler", "icon": "refresh-cw", "priority": 4}
                ],
                "kpis": {
                    "loan_approval_rate": "Kredi Onay Oranı",
                    "portfolio_performance": "Portföy Performansı",
                    "new_accounts": "Yeni Hesaplar",
                    "transaction_volume": "İşlem Hacmi"
                }
            },
            "retail": {
                **base_config,
                "title": "Perakende Satış Dashboard",
                "theme": {
                    "primary_color": "#8b5cf6",
                    "accent_color": "#a855f7",
                    "background": "bg-gradient-to-br from-purple-900 via-violet-800 to-indigo-900"
                },
                "widgets": [
                    {"id": "daily_sales", "title": "Günlük Satış", "icon": "shopping-bag", "priority": 1},
                    {"id": "inventory_levels", "title": "Stok Seviyeleri", "icon": "package", "priority": 2},
                    {"id": "customer_footfall", "title": "Müşteri Trafiği", "icon": "users", "priority": 3},
                    {"id": "conversion_rate", "title": "Dönüşüm Oranı", "icon": "trending-up", "priority": 4}
                ],
                "kpis": {
                    "sales_volume": "Satış Hacmi",
                    "inventory_turnover": "Stok Devir Hızı",
                    "average_basket": "Ortalama Sepet",
                    "customer_return_rate": "Müşteri Geri Dönüş"
                }
            }
        }
        
        return sector_configs.get(sector, sector_configs["beauty"])

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()