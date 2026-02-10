
import asyncio
import bcrypt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.tenant import Tenant
from app.models.customer import Customer
from app.core.encryption import encryption_service
import uuid

# Define users to seed
SECTOR_USERS = [
    {
        "sector": "medical",
        "customer_id": "MED-000001",
        "name": "Dr. Medical User",
        "email": "med.user@example.com",
        "tenant_name": "City General Hospital"
    },
    {
        "sector": "legal",
        "customer_id": "LEG-000001",
        "name": "Adv. Legal User",
        "email": "leg.user@example.com",
        "tenant_name": "Legal Partners LLC"
    },
    {
        "sector": "real_estate",
        "customer_id": "EST-000001",
        "name": "Real Estate Agent",
        "email": "est.user@example.com",
        "tenant_name": "Prime Properties"
    },
    {
        "sector": "finance",
        "customer_id": "FIN-000001",
        "name": "Financial Advisor",
        "email": "fin.user@example.com",
        "tenant_name": "Global Finance Corp"
    },
    {
        "sector": "technology",
        "customer_id": "TEC-000001",
        "name": "Tech Admin",
        "email": "tec.user@example.com",
        "tenant_name": "NextGen Tech"
    }
]

PIN = "1234"

async def seed_users():
    print("🚀 Starting sector user seeding...")
    
    # Create engine
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Hash PIN (bcrypt)
        salt = bcrypt.gensalt()
        pin_hash = bcrypt.hashpw(PIN.encode('utf-8'), salt).decode('utf-8')
        
        for user_data in SECTOR_USERS:
            print(f"Processing {user_data['sector']}...")
            
            # 1. Check/Create Tenant
            query = select(Tenant).where(Tenant.name == user_data['tenant_name'])
            result = await session.execute(query)
            tenant = result.scalar_one_or_none()
            
            if not tenant:
                print(f"Creating tenant: {user_data['tenant_name']}")
                tenant = Tenant(
                    name=user_data['tenant_name'],
                    slug=user_data['sector'],
                    config={"sector": user_data['sector']}
                )
                session.add(tenant)
                await session.flush() # get ID
            else:
                print(f"Tenant exists: {tenant.name}")
                # Ensure config has sector
                if not tenant.config or tenant.config.get('sector') != user_data['sector']:
                   tenant.config = {"sector": user_data['sector']}
            
            # 2. Check/Create Customer
            query = select(Customer).where(Customer.customer_id == user_data['customer_id'])
            result = await session.execute(query)
            customer = result.scalar_one_or_none()
            
            if not customer:
                print(f"Creating customer: {user_data['customer_id']}")
                customer = Customer(
                    first_name=user_data['name'].split(' ')[0],
                    last_name=' '.join(user_data['name'].split(' ')[1:]),
                    email=user_data['email'],
                    customer_id=user_data['customer_id'],
                    pin_hash=pin_hash,
                    tenant_id=tenant.id,
                    phone_hash="dummy_hash_" + user_data['sector'], # Dummy for unique constraint if needed, or rely on encryption service
                    # encryption service helper handles setting phone and hash
                )
                # Use encryption service helper to set dummy phone
                dummy_phone = f"+90555000{str(SECTOR_USERS.index(user_data)).zfill(4)}"
                customer.set_phone(dummy_phone)
                
                session.add(customer)
            else:
                print(f"Customer exists: {user_data['customer_id']}. Updating PIN/Tenant.")
                customer.pin_hash = pin_hash
                customer.tenant_id = tenant.id
            
        await session.commit()
    
    await engine.dispose()
    print("✅ Seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_users())
