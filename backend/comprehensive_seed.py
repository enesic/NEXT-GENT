"""
Comprehensive seed script for NEXT-GENT demo.
Creates realistic data for multiple sectors.
"""
import asyncio
import os
import sys
import random
from datetime import datetime, timedelta
from uuid import uuid4

# Add backend directory to python path
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.customer import Customer, CustomerSegment, CustomerStatus
from app.models.interaction import Interaction, InteractionStatus
from app.models.satisfaction import Satisfaction

# Sector definitions with realistic data
SECTORS = {
    "medical": {
        "name": "NextGent Sağlık",
        "slug": "nextgent-saglik",
        "domain": "hospital.com",
        "interaction_types": ["Kontrol", "İlk Muayene", "Tahlil", "Tedavi", "Aşı"],
        "example_emails": ["doktor@hospital.com", "hekim@clinic.com", "doctor@medical.com"]
    },
    "legal": {
        "name": "NextGent Hukuk",
        "slug": "nextgent-hukuk",
        "domain": "lawfirm.com",
        "interaction_types": ["Danışma", "Dava Takibi", "Sözleşme", "Arabuluculuk", "Mahkeme"],
        "example_emails": ["avukat@lawfirm.com", "lawyer@legal.com", "hukuk@avukatlik.com"]
    },
    "real_estate": {
        "name": "NextGent Emlak",
        "slug": "nextgent-emlak",
        "domain": "realty.com",
        "interaction_types": ["Konut Gezisi", "Ofis Gezisi", "Değerleme", "Sözleşme", "Teslim"],
        "example_emails": ["danışman@emlak.com", "agent@realty.com", "konut@gayrimenkul.com"]
    },
    "manufacturing": {
        "name": "NextGent Sanayi",
        "slug": "nextgent-sanayi",
        "domain": "factory.com",
        "interaction_types": ["Üretim Planlama", "Kalite Kontrol", "Bakım", "Tedarik", "Sevkiyat"],
        "example_emails": ["mudur@fabrika.com", "manager@factory.com", "uretim@sanayi.com"]
    },
    "ecommerce": {
        "name": "NextGent E-Ticaret",
        "slug": "nextgent-eticaret",
        "domain": "shop.com",
        "interaction_types": ["Sipariş Takibi", "İade", "Müşteri Desteği", "Ürün Danışma", "Kargo"],
        "example_emails": ["destek@shop.com", "support@ecommerce.com", "musteri@magaza.com"]
    },
    "education": {
        "name": "NextGent Eğitim",
        "slug": "nextgent-egitim",
        "domain": "school.com",
        "interaction_types": ["Ders", "Sınav", "Veli Görüşmesi", "Danışmanlık", "Etkinlik"],
        "example_emails": ["ogretmen@okul.com", "teacher@school.com", "egitim@academy.com"]
    },
    "finance": {
        "name": "NextGent Finans",
        "slug": "nextgent-finans",
        "domain": "bank.com",
        "interaction_types": ["Kredi Başvuru", "Yatırım Danışma", "Hesap Açma", "Sigorta", "Bütçe"],
        "example_emails": ["musavirbanka.com", "advisor@finance.com", "finans@bank.com"]
    },
    "hospitality": {
        "name": "NextGent Otelcilik",
        "slug": "nextgent-otelcilik",
        "domain": "hotel.com",
        "interaction_types": ["Rezervasyon", "Check-in", "Etkinlik", "Spa", "Restoran"],
        "example_emails": ["resepsiyon@hotel.com", "reception@resort.com", "otel@hospitality.com"]
    },
    "automotive": {
        "name": "NextGent Otomotiv",
        "slug": "nextgent-otomotiv",
        "domain": "dealer.com",
        "interaction_types": ["Test Sürüşü", "Servis", "Bakım", "Satış", "Aksesuar"],
        "example_emails": ["satis@galeri.com", "sales@dealer.com", "servis@automotive.com"]
    },
    "retail": {
        "name": "NextGent Perakende",
        "slug": "nextgent-perakende",
        "domain": "store.com",
        "interaction_types": ["Satış", "Değişim", "Danışma", "Stok Bilgi", "Kampanya"],
        "example_emails": ["magaza@store.com", "shop@retail.com", "satis@perakende.com"]
    }
}

# Turkish names for realistic data
FIRST_NAMES = ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Mustafa", "Zeynep", "Elif", "Can", "Ece"]
LAST_NAMES = ["Yılmaz", "Demir", "Çelik", "Kaya", "Arslan", "Şahin", "Öztürk", "Koç", "Aydın", "Polat"]

async def create_tenants(db):
    """Create tenant for each sector."""
    print("\n📊 Creating tenants...")
    tenants = {}
    
    for sector_key, sector_data in SECTORS.items():
        tenant = Tenant(
            name=sector_data["name"],
            slug=sector_data["slug"],
            domain=sector_data["domain"],
            is_active=True,
            config={"sector": sector_key},
            system_prompt=f"Sen {sector_data['name']} için özel AI asistansın."
        )
        db.add(tenant)
        await db.flush()
        tenants[sector_key] = tenant
        print(f"  ✅ {sector_data['name']} ({sector_key})")
    
    await db.commit()
    return tenants

async def create_customers(db, tenants):
    """Create customers for each tenant."""
    print("\n👥 Creating customers...")
    import bcrypt
    
    customers = {}
    customer_phones = {}  # Store phone numbers separately to avoid lazy loading issues
    
    # Sector code mapping
    sector_codes = {
        "medical": "MED",
        "legal": "LEG",
        "real_estate": "EST",
        "manufacturing": "MFG",
        "ecommerce": "ECM",
        "education": "EDU",
        "finance": "FIN",
        "hospitality": "HTL",
        "automotive": "AUTO",
        "retail": "RTL"
    }
    
    for sector_key, tenant in tenants.items():
        sector_customers = []
        sector_code = sector_codes.get(sector_key, "GEN")
        
        #20 customers per sector
        for i in range(20):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            
            # Generate customer ID: SECTOR-NNNNNN
            customer_number = str(i + 1).zfill(6)  # 000001, 000002, etc.
            customer_id = f"{sector_code}-{customer_number}"
            
            # Generate PIN (default: 1234 for demo, hashed with bcrypt)
            default_pin = "1234"
            pin_hash = bcrypt.hashpw(default_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Varied segments
            if i < 2:
                segment = CustomerSegment.VIP
                total_spent = random.uniform(15000, 50000)
                total_orders = random.randint(60, 150)
            elif i < 5:
                segment = CustomerSegment.GOLD
                total_spent = random.uniform(7000, 15000)
                total_orders = random.randint(30, 60)
            elif i < 10:
                segment = CustomerSegment.SILVER
                total_spent = random.uniform(2000, 7000)
                total_orders = random.randint(15, 30)
            else:
                segment = CustomerSegment.REGULAR
                total_spent = random.uniform(100, 2000)
                total_orders = random.randint(1, 15)
            
            # Generate phone number
            phone_number = f"+905{random.randint(300000000, 599999999)}"
            
            customer = Customer(
                tenant_id=tenant.id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                customer_id=customer_id,
                pin_hash=pin_hash,
                segment=segment,
                status=CustomerStatus.ACTIVE,
                total_orders=total_orders,
                total_spent=total_spent,
                lifetime_value=total_spent * 1.2,
                notes=f"{sector_key.title()} sektöründen müşteri",
                phone_hash=Customer.generate_phone_hash(phone_number)  # Set hash directly
            )
            # Set phone with encryption
            customer.set_phone(phone_number)
            db.add(customer)
            sector_customers.append(customer)
            
            # Store phone number for later use
            customer_phones[id(customer)] = phone_number
        
        await db.flush()
        customers[sector_key] = sector_customers
        print(f"  ✅ {len(sector_customers)} customers for {sector_key} (IDs: {sector_code}-000001 to {sector_code}-{customer_number})")
    
    await db.commit()
    return customers, customer_phones

async def create_interactions(db, tenants, customers, customer_phones):
    """Create interactions (appointments) for each tenant."""
    print("\n📅 Creating interactions...")
    
    from sqlalchemy.exc import IntegrityError
    
    base_time = datetime.utcnow()
    total_created = 0
    
    for sector_key, tenant in tenants.items():
        sector_types = SECTORS[sector_key]["interaction_types"]
        sector_customers = customers[sector_key]
        
        # 50 interactions per sector across 30 days
        for i in range(50):
            days_ago = random.randint(0, 30)
            target_date = base_time - timedelta(days=days_ago)
            
            # Business hours
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            start = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            end = start + timedelta(minutes=random.choice([30, 45, 60]))
            
            # Status distribution
            if days_ago > 7:
                status = random.choice([InteractionStatus.COMPLETED, InteractionStatus.CANCELLED])
            elif days_ago > 0:
                status = InteractionStatus.CONFIRMED
            else:
                status = random.choice([InteractionStatus.CONFIRMED, InteractionStatus.PENDING])
            
            customer = random.choice(sector_customers)
            customer_full_name = f"{customer.first_name} {customer.last_name}"
            customer_phone = customer_phones.get(id(customer), "+905000000000")  # Get from dict
            
            interaction = Interaction(
                tenant_id=tenant.id,
                title=random.choice(sector_types),
                description=f"Otomatik oluşturulmuş {sector_key} randevusu",
                type=random.choice(sector_types).lower().replace(' ', '_'),
                start_time=start,
                end_time=end,
                client_name=customer_full_name,
                client_email=customer.email,
                client_phone=customer_phone,
                status=status,
                created_at=start - timedelta(days=random.randint(1, 5))
            )
            
            try:
                db.add(interaction)
                await db.commit()
                total_created += 1
            except IntegrityError:
                await db.rollback()
                # Skip overlapping appointments
                continue
        
        print(f"  ✅ {sector_key}: Interactions created")
    
    print(f"\n  📊 Total: {total_created} interactions across all sectors")
    return total_created

async def create_satisfaction_data(db, tenants):
    """Create satisfaction survey responses."""
    print("\n⭐ Creating satisfaction data...")
    
    base_time = datetime.utcnow()
    total_created = 0
    
    for sector_key, tenant in tenants.items():
        # 30 satisfaction responses per sector
        for i in range(30):
            days_ago = random.randint(0, 30)
            
            # Varied CSAT ratings (1-5 stars)
            csat = random.choices(
                [1, 2, 3, 4, 5],
                weights=[5, 10, 20, 35, 30]  # More positive ratings
            )[0]
            
            # NPS score (0-10)
            nps = random.choices(
                range(11),
                weights=[2, 3, 5, 6, 8, 10, 12, 15, 18, 12, 9]
            )[0]
            
            # Sentiment based on CSAT rating
            if csat >= 4:
                sentiment = "positive"
                score = random.uniform(0.7, 1.0)
            elif csat == 3:
                sentiment = "neutral"
                score = random.uniform(0.4, 0.6)
            else:
                sentiment = "negative"
                score = random.uniform(0.0, 0.3)
            
            satisfaction = Satisfaction(
                tenant_id=tenant.id,
                interaction_id=None,  # Can be linked later
                customer_id=None,
                survey_type="csat",
                channel="in_app",
                csat_score=csat,
                nps_score=nps,
                feedback_text=f"Demo feedback for {sector_key} sector",
                sentiment=sentiment,
                sentiment_score=score,
                responded_at=base_time - timedelta(days=days_ago),
                survey_sent_at=base_time - timedelta(days=days_ago, hours=2)
            )
            db.add(satisfaction)
            total_created += 1
        
        print(f"  ✅ {sector_key}: 30 satisfaction responses")
    
    await db.commit()
    print(f"\n  📊 Total: {total_created} satisfaction responses")

async def seed():
    """Main seeding function."""
    print("="*60)
    print("🌱 COMPREHENSIVE SEED DATA GENERATION")
    print("="*60)
    
    async with AsyncSessionLocal() as db:
        # Clear existing data
        print("\n🗑️  Clearing existing data...")
        from sqlalchemy import delete
        await db.execute(delete(Satisfaction))
        await db.execute(delete(Interaction))
        await db.execute(delete(Customer))
        await db.execute(delete(Tenant))
        await db.commit()
        print("  ✅ Database cleared")
        
        # Create data
        tenants = await create_tenants(db)
        customers, customer_phones = await create_customers(db, tenants)
        await create_interactions(db, tenants, customers, customer_phones)
        await create_satisfaction_data(db, tenants)
        
        print("\n" + "="*60)
        print("✅ SEEDING COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Tenants: {len(tenants)}")
        print(f"   • Customers: {sum(len(c) for c in customers.values())}")
        print(f"   • Sectors: {', '.join(SECTORS.keys())}")
        print("\n🔐 Login with Customer ID + PIN:")
        print("   Default PIN for all accounts: 1234")
        print("\n🎯 Demo Accounts (Customer ID format):")
        for sector_key, sector_data in SECTORS.items():
            sector_code = {
                "medical": "MED", "legal": "LEG", "real_estate": "EST",
                "manufacturing": "MFG", "ecommerce": "ECM", "education": "EDU",
                "finance": "FIN", "hospitality": "HTL", "automotive": "AUTO",
                "retail": "RTL"
            }.get(sector_key, "GEN")
            print(f"   • {sector_data['name']}: {sector_code}-000001 (PIN: 1234)")
        print("\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
