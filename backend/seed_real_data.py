import asyncio
import os
import sys
import random
from datetime import datetime, timedelta

# Add backend directory to python path for imports
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.interaction import Interaction, InteractionStatus

async def seed():
    print("Seeding database...")
    async with AsyncSessionLocal() as db:
        # 1. Tenant
        from sqlalchemy import select
        res = await db.execute(select(Tenant).limit(1))
        tenant = res.scalar_one_or_none()
        if not tenant:
            tenant = Tenant(
                name="NextGent Medical", 
                slug="nextgent-medical", 
                config={"sector": "medical"}
            )
            db.add(tenant)
            await db.commit()
            await db.refresh(tenant)
            print(f"Created Tenant: {tenant.name}")
        else:
            print(f"Using Tenant: {tenant.name}")

        # 2. Interactions
        interactions = []
        base_time = datetime.utcnow()
        names = ["Ahmet Yılmaz", "Ayşe Demir", "Mehmet Kaya", "Fatma Çelik", "Mustafa Şahin"]
        
        for i in range(100):
            days_ago = random.randint(0, 30)
            # Make Tuesdays busy
            target_date = base_time - timedelta(days=days_ago)
            if i % 3 == 0:
                  while target_date.weekday() != 1:
                        days_ago = random.randint(0, 30)
                        target_date = base_time - timedelta(days=days_ago)
            
            # Make 16:00 risky
            is_risky = (i % 10 == 0)
            hour = 16 if is_risky else random.randint(9, 17)
            minute = random.choice([0, 15, 30])
            start = target_date.replace(hour=hour, minute=minute)
            end = start + timedelta(minutes=45)
            
            status = InteractionStatus.CANCELLED if is_risky else random.choice([InteractionStatus.CONFIRMED, InteractionStatus.COMPLETED])
            
            intr = Interaction(
                tenant_id=tenant.id,
                title=f"Randevu {i}",
                description="Auto generated",
                type="appointment",
                start_time=start,
                end_time=end,
                client_name=random.choice(names),
                client_email="test@example.com",
                client_phone="5551234567",
                status=status,
                created_at=start - timedelta(days=2)
            )
            interactions.append(intr)
            
        # Insert one by one to handle overlaps gracefully
        from sqlalchemy.exc import IntegrityError
        
        success_count = 0
        for interaction in interactions:
            try:
                db.add(interaction)
                await db.commit()
                success_count += 1
            except IntegrityError:
                await db.rollback()
                print(f"Skipping overlapping interaction at {interaction.start_time}")
            except Exception as e:
                await db.rollback()
                print(f"Error inserting interaction: {e}")
                
        print(f"Seeded {success_count} interactions successfully.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
