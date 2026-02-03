import asyncio
import os
import sys
import bcrypt
import random
from datetime import datetime, timedelta
from sqlalchemy import select

# Ensure we can import app modules
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.customer import Customer, CustomerSegment, CustomerStatus
from app.models.interaction import Interaction, InteractionStatus

# Define manual class if not imported correctly (as fallback) or rely on app.models
# Assuming imports work as file is in backend/ root

async def seed_sectors():
    print("🌍 Starting Multi-Sector Seeding...")
    
    # Define Sectors
    sectors = [
        {
            "slug": "nextgent-medical",
            "name": "NextGent Hastaneler Grubu",
            "sector": "medical",
            "user_id": "MED-001234",
            "user_name": "Dr. Ahmet Yılmaz",
            "interactions": [
                {"title": "Check-up Kontrolü", "type": "Muayene"},
                {"title": "Diş Temizliği", "type": "Tedavi"},
                {"title": "Kardiyoloji Konsültasyonu", "type": "Muayene"},
                {"title": "Kan Tahlili Sonuçları", "type": "Laboratuvar"}
            ]
        },
        {
            "slug": "nextgent-legal",
            "name": "NextGent Hukuk Bürosu",
            "sector": "legal",
            "user_id": "LAW-005678",
            "user_name": "Av. Mehmet Demir",
            "interactions": [
                {"title": "Boşanma Davası Duruşması", "type": "Duruşma"},
                {"title": "Şirket Birleşmesi Görüşmesi", "type": "Toplantı"},
                {"title": "İcra Takibi Başvurusu", "type": "İcra"},
                {"title": "Müvekkil Bilgilendirme", "type": "Görüşme"}
            ]
        },
        {
            "slug": "nextgent-real-estate",
            "name": "NextGent Gayrimenkul Yatırım",
            "sector": "real_estate",
            "user_id": "EST-009101",
            "user_name": "Canan Emlak",
            "interactions": [
                {"title": "Villa Gösterimi - Çekmeköy", "type": "Sunum"},
                {"title": "Kiralama Sözleşmesi İmza", "type": "İmza"},
                {"title": "Tapu Devir İşlemleri", "type": "Tapu"},
                {"title": "Ekspertiz Raporu İncelemesi", "type": "Analiz"}
            ]
        },
        {
            "slug": "nextgent-retail",
            "name": "NextGent Mağazacılık A.Ş.",
            "sector": "retail",
            "user_id": "RET-002233",
            "user_name": "Mağaza Müdürü Selin",
            "interactions": [
                {"title": "Stok Sayım Kontrolü", "type": "Operasyon"},
                {"title": "Tedarikçi Görüşmesi", "type": "Satınalma"},
                {"title": "Müşteri İade İşlemi", "type": "Müşteri Hizm."},
                {"title": "Kampanya Planlama", "type": "Pazarlama"}
            ]
        },
        {
            "slug": "nextgent-manufacturing",
            "name": "NextGent Sanayi",
            "sector": "manufacturing",
            "user_id": "MAN-004455",
            "user_name": "Müh. Kemal Usta",
            "interactions": [
                {"title": "CNC Bakım Planlaması", "type": "Bakım"},
                {"title": "Hammadde Giriş Kontrolü", "type": "Kalite"},
                {"title": "Vardiya Amirleri Toplantısı", "type": "Yönetim"},
                {"title": "ISO Denetim Hazırlığı", "type": "Denetim"}
            ]
        },
        {
            "slug": "nextgent-education",
            "name": "NextGent Koleji",
            "sector": "education",
            "user_id": "EDU-006677",
            "user_name": "Müdür Ayşe Hanım",
            "interactions": [
                {"title": "Veli Toplantısı - Lise", "type": "Toplantı"},
                {"title": "Öğretmenler Kurulu", "type": "Kurul"},
                {"title": "Yeni Kayıt Görüşmesi", "type": "Kayıt"},
                {"title": "Rehberlik Servisi Raporu", "type": "Raporlama"}
            ]
        },
        {
            "slug": "nextgent-automotive",
            "name": "NextGent Otomotiv Servis",
            "sector": "automotive",
            "user_id": "AUTO-008899",
            "user_name": "Servis Danışmanı Ali",
            "interactions": [
                {"title": "Periyodik Bakım - 34 ABC 12", "type": "Bakım"},
                {"title": "Hasar Tespiti ve Ekspertiz", "type": "Ekspertiz"},
                {"title": "Yedek Parça Siparişi", "type": "Lojistik"},
                {"title": "Müşteri Teslimat Süreci", "type": "Teslimat"}
            ]
        }
    ]

    async with AsyncSessionLocal() as db:
        pin_hash = bcrypt.hashpw(b"1234", bcrypt.gensalt()).decode('utf-8')

        for sector_data in sectors:
            print(f"\n🚀 Processing: {sector_data['name']} ({sector_data['sector']})")

            # 1. Create/Get Tenant
            res = await db.execute(select(Tenant).where(Tenant.slug == sector_data['slug']))
            tenant = res.scalar_one_or_none()
            
            if not tenant:
                tenant = Tenant(
                    name=sector_data['name'], 
                    slug=sector_data['slug'], 
                    config={"sector": sector_data['sector'], "displayName": sector_data['name']}
                )
                db.add(tenant)
                await db.commit()
                await db.refresh(tenant)
                print(f"✅ Created Tenant: {tenant.name}")
            else:
                # Update config just in case
                tenant.config = {"sector": sector_data['sector'], "displayName": sector_data['name']}
                db.add(tenant) 
                
            # 2. Create/Update User (Customer)
            user_id = sector_data['user_id']
            # Use query to find existing user
            res = await db.execute(select(Customer).where(Customer.customer_id == user_id))
            user = res.scalar_one_or_none()
            
            fullname = sector_data['user_name'].split(' ')
            first_name = fullname[0]
            last_name = ' '.join(fullname[1:]) if len(fullname) > 1 else ''
            
            if not user:
                user = Customer(
                    tenant_id=tenant.id,
                    customer_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=f"{sector_data['sector']}@nextgent.com",
                    phone=f"+90555{random.randint(1000000, 9999999)}",
                    segment=CustomerSegment.VIP,
                    status=CustomerStatus.ACTIVE,
                    pin_hash=pin_hash
                )
                db.add(user)
                print(f"✅ Created User: {user_id}")
            else:
                user.pin_hash = pin_hash # Reset PIN
                user.tenant_id = tenant.id # Ensure correct tenant (though slug should match)
                print(f"ℹ️ User {user_id} exists.")

            await db.commit()
            
            # Need to fetch fresh tenant ID for interactions if we just created/updated user
            # Actually we rely on 'tenant' object which is refreshed or loaded.

            # 3. Create Interactions (Seed Data)
            # Check count
            res = await db.execute(select(Interaction).where(Interaction.tenant_id == tenant.id))
            count = len(res.all())
            
            if count < 5:
                print("🌱 Seeding interactions...")
                for i in range(5):
                    data = random.choice(sector_data['interactions'])
                    status = random.choice([InteractionStatus.CONFIRMED, InteractionStatus.PENDING, InteractionStatus.COMPLETED, InteractionStatus.CANCELLED])
                    
                    start = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                    duration = random.randint(30, 120)
                    
                    interaction = Interaction(
                        tenant_id=tenant.id,
                        title=f"{data['title']} #{random.randint(100, 999)}",
                        type=data['type'],
                        description=f"{data['title']} detaylı açıklama metni...",
                        start_time=start,
                        end_time=start + timedelta(minutes=duration),
                        client_name=f"Client {random.randint(1, 100)}",
                        client_email=f"client{random.randint(1, 100)}@example.com",
                        client_phone="+905551234567",
                        status=status,
                        version=1
                    )
                    db.add(interaction)
                await db.commit()
                print("✅ Seeded interactions.")

    print("\n✨ All Sectors Seeded Successfully!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_sectors())
