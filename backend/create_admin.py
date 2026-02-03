import asyncio
import os
import sys
import bcrypt
from sqlalchemy import select

# Ensure we can import app modules
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.customer import Customer, CustomerSegment, CustomerStatus

async def create_admin():
    print("Creating Admin User...")
    async with AsyncSessionLocal() as db:
        # 1. Ensure Tenant
        res = await db.execute(select(Tenant).limit(1))
        tenant = res.scalar_one_or_none()
        
        if not tenant:
            print("Tenant not found. Creating default tenant...")
            tenant = Tenant(
                name="NextGent Medical", 
                slug="nextgent-medical", 
                config={"sector": "medical"}
            )
            db.add(tenant)
            await db.commit()
            await db.refresh(tenant)
        
        print(f"Using Tenant: {tenant.name} ({tenant.id})")

        # 2. Check if Customer exists
        CUSTOMER_ID = "MED-001234"
        query = select(Customer).where(Customer.customer_id == CUSTOMER_ID)
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"User {CUSTOMER_ID} already exists. Updating PIN to 1234...")
            # Update PIN just in case
            pin_hash = bcrypt.hashpw(b"1234", bcrypt.gensalt()).decode('utf-8')
            existing_user.pin_hash = pin_hash
            await db.commit()
            print("PIN updated.")
            return

        # 3. Create Customer
        print(f"Creating user {CUSTOMER_ID}...")
        pin_hash = bcrypt.hashpw(b"1234", bcrypt.gensalt()).decode('utf-8')
        
        customer = Customer(
            tenant_id=tenant.id,
            customer_id=CUSTOMER_ID,
            first_name="Dr. Ahmet",
            last_name="Yilmaz",
            email="ahmet.yilmaz@nextgent.com",
            phone="+905550001234",
            segment=CustomerSegment.VIP,
            status=CustomerStatus.ACTIVE,
            pin_hash=pin_hash
        )
        
        db.add(customer)
        await db.commit()
        print(f"✅ SUCCESS! Created user: {CUSTOMER_ID} / PIN: 1234")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_admin())
