#!/usr/bin/env python3
"""
Create sectoral customer data for NextGent system
Generates KVKK-compliant fake data for all sectors
"""
import asyncio
import asyncpg
import bcrypt
import json
from faker import Faker
from faker.providers import automotive, company, date_time, internet, person, phone_number
import hashlib
import random

# Initialize faker with Turkish locale
fake = Faker(['tr_TR', 'en_US'])

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Sector configurations
SECTORS = {
    'beauty': {
        'tenant_name': 'Güzellik & Estetik',
        'customers': ['BEA-000001', 'BEA-000002', 'BEA-000003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['güzellik salonu', 'kuaför', 'estetik merkezi', 'SPA']
    },
    'automotive': {
        'tenant_name': 'Otomotiv',
        'customers': ['AUTO-001', 'AUTO-002', 'AUTO-003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['oto galeri', 'servis', 'yedek parça', 'lastik']
    },
    'retail': {
        'tenant_name': 'Perakende',
        'customers': ['RET-0001', 'RET-0002', 'RET-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['mağaza', 'market', 'butik', 'outlet']
    },
    'finance': {
        'tenant_name': 'Finans',
        'customers': ['FIN-0001', 'FIN-0002', 'FIN-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['banka', 'sigorta', 'yatırım', 'danışmanlık']
    },
    'medical': {
        'tenant_name': 'Sağlık',
        'customers': ['MED-0001', 'MED-0002', 'MED-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['hastane', 'poliklinik', 'diş kliniği', 'laboratuvar']
    },
    'hospitality': {
        'tenant_name': 'Otelcilik',
        'customers': ['HOTEL-01', 'HOTEL-02', 'HOTEL-03'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['otel', 'pansiyon', 'resort', 'butik otel']
    },
    'education': {
        'tenant_name': 'Eğitim',
        'customers': ['EDU-0001', 'EDU-0002', 'EDU-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['okul', 'kurs', 'üniversite', 'kreş']
    },
    'legal': {
        'tenant_name': 'Hukuk',
        'customers': ['LAW-0001', 'LAW-0002', 'LAW-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['hukuk bürosu', 'avukat', 'noterlik', 'icra']
    },
    'manufacturing': {
        'tenant_name': 'İmalat',
        'customers': ['MFG-0001', 'MFG-0002', 'MFG-0003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['fabrika', 'atölye', 'üretim', 'montaj']
    },
    'realestate': {
        'tenant_name': 'Emlak',
        'customers': ['RE-00001', 'RE-00002', 'RE-00003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['emlak ofisi', 'gayrimenkul', 'inşaat', 'konut']
    },
    'ecommerce': {
        'tenant_name': 'E-ticaret',
        'customers': ['EC-00001', 'EC-00002', 'EC-00003'],
        'pins': ['1234', '5678', '9012'],
        'company_types': ['online mağaza', 'e-ticaret', 'dijital', 'marketplace']
    }
}

def encrypt_phone(phone: str) -> str:
    """KVKK compliant phone hashing"""
    return hashlib.sha256(phone.encode()).hexdigest()

def generate_customer_profile(sector: str, customer_id: str, pin: str):
    """Generate realistic customer profile"""
    company_type = random.choice(SECTORS[sector]['company_types'])
    
    # KVKK compliant fake data
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # Masked email for privacy
    domain = fake.domain_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
    
    # Generate PIN hash
    pin_hash = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Generate phone and hash it (KVKK compliance)
    phone = fake.phone_number()
    phone_hash = encrypt_phone(phone)
    
    # Random customer metrics
    segment = random.choice(['regular', 'silver', 'gold', 'vip'])
    total_orders = random.randint(1, 100)
    total_spent = round(random.uniform(100, 10000), 2)
    lifetime_value = round(total_spent * random.uniform(1.1, 2.0), 2)
    
    return {
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'pin_hash': pin_hash,
        'phone_hash': phone_hash,
        'segment': segment,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'lifetime_value': lifetime_value,
        'company_type': company_type
    }

async def create_sectoral_data():
    """Create all sectoral data"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Creating sectoral tenants and customers...")
        
        # Create tenants for each sector
        for sector, config in SECTORS.items():
            print(f"Processing sector: {sector}")
            
            # Create tenant
            tenant_id = await conn.fetchval("""
                INSERT INTO tenants (name, slug, domain, is_active, config)
                VALUES ($1, $2, 'nextgent.co', TRUE, $3)
                ON CONFLICT (slug) DO UPDATE SET 
                    name = EXCLUDED.name,
                    config = EXCLUDED.config
                RETURNING id
            """, config['tenant_name'], sector, json.dumps({"sector": sector}))
            
            print(f"  > Tenant created: {config['tenant_name']} (ID: {tenant_id})")
            
            # Create customers for this sector
            for i, (customer_id, pin) in enumerate(zip(config['customers'], config['pins'])):
                profile = generate_customer_profile(sector, customer_id, pin)
                
                await conn.execute("""
                    INSERT INTO customers (
                        tenant_id, customer_id, first_name, last_name, 
                        email, pin_hash, phone_hash, segment, status,
                        total_orders, total_spent, lifetime_value
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'active', $9, $10, $11)
                    ON CONFLICT (customer_id) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        email = EXCLUDED.email,
                        pin_hash = EXCLUDED.pin_hash,
                        phone_hash = EXCLUDED.phone_hash,
                        segment = EXCLUDED.segment,
                        total_orders = EXCLUDED.total_orders,
                        total_spent = EXCLUDED.total_spent,
                        lifetime_value = EXCLUDED.lifetime_value
                """, 
                tenant_id, customer_id, profile['first_name'], profile['last_name'],
                profile['email'], profile['pin_hash'], profile['phone_hash'], 
                profile['segment'], profile['total_orders'], profile['total_spent'], 
                profile['lifetime_value'])
                
                print(f"    - Customer: {customer_id} ({profile['first_name']} {profile['last_name']}) - PIN: {pin}")
        
        # Generate demo call interactions using the new table
        print("\nGenerating demo call interactions...")
        
        # Generate for all sectors
        all_tenants = await conn.fetch("SELECT id, slug FROM tenants WHERE slug != 'nextgent-main'")
        
        for tenant in all_tenants:
            tenant_customers = await conn.fetch("SELECT id, customer_id FROM customers WHERE tenant_id = $1 LIMIT 2", tenant['id'])
            
            interaction_types = ['support', 'sales', 'complaint', 'inquiry', 'technical', 'billing']
            resolution_statuses = ['resolved', 'pending', 'escalated', 'closed']
            agent_names = ['Ayşe Yılmaz', 'Mehmet Demir', 'Fatma Şahin', 'Ali Kaya', 'Zeynep Özkan']
            
            for customer in tenant_customers:
                for _ in range(random.randint(5, 15)):  # More interactions per customer
                    interaction_type = random.choice(interaction_types)
                    satisfaction = random.randint(1, 5)
                    duration = random.randint(30, 900)  # 30 seconds to 15 minutes
                    resolution_status = random.choice(resolution_statuses)
                    agent_name = random.choice(agent_names)
                    days_ago = random.randint(0, 90)
                    
                    await conn.execute("""
                        INSERT INTO call_interactions (
                            tenant_id, customer_id, interaction_type, 
                            call_duration_seconds, satisfaction_score,
                            resolution_status, agent_name,
                            call_timestamp, call_summary
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW() - INTERVAL '%s days', $8)
                    """ % days_ago, tenant['id'], customer['id'], interaction_type, 
                    duration, satisfaction, resolution_status, agent_name,
                    f"{interaction_type.capitalize()} call handled by {agent_name}")
        
        print("Call interactions created!")
        
        # Generate analytics metrics for each sector
        print("Generating analytics metrics...")
        
        metrics_to_generate = [
            'total_calls', 'avg_call_duration', 'customer_satisfaction',
            'resolution_rate', 'first_call_resolution', 'revenue',
            'new_customers', 'active_users', 'conversion_rate'
        ]
        
        for tenant in all_tenants:
            for metric in metrics_to_generate:
                for days_back in range(30):  # 30 days of data
                    value = round(random.uniform(10, 1000), 2)
                    if metric == 'customer_satisfaction':
                        value = round(random.uniform(3.5, 5.0), 1)
                    elif metric == 'resolution_rate':
                        value = round(random.uniform(75, 98), 1)
                    elif metric == 'conversion_rate':
                        value = round(random.uniform(15, 45), 1)
                    
                    await conn.execute("""
                        INSERT INTO analytics_metrics (
                            tenant_id, metric_name, metric_value, metric_date
                        ) VALUES ($1, $2, $3, CURRENT_DATE - INTERVAL '%s days')
                        ON CONFLICT (tenant_id, metric_name, metric_date, metric_period) 
                        DO NOTHING
                    """ % days_back, tenant['id'], metric, value)
        
        print("Analytics metrics created!")
        
        print("\nSECTORAL DATA CREATION COMPLETE!")
        print("\nLOGIN CREDENTIALS BY SECTOR:")
        print("="*50)
        
        for sector, config in SECTORS.items():
            print(f"\n{config['tenant_name'].upper()} ({sector})")
            for customer_id, pin in zip(config['customers'], config['pins']):
                print(f"  {customer_id} / PIN: {pin}")
        
        print("\nADMIN LOGIN:")
        print("  admin / admin123")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_sectoral_data())