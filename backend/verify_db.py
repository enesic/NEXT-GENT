"""Quick database verification script"""
import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import select, func
from app.models.tenant import Tenant
from app.models.customer import Customer
from app.models.interaction import Interaction
from app.models.vapi_call import VAPICall
from app.models.token_usage import TokenUsage

async def verify():
    async with AsyncSessionLocal() as db:
        # Count records
        tenant_count = await db.scalar(select(func.count(Tenant.id)))
        customer_count = await db.scalar(select(func.count(Customer.id)))
        interaction_count = await db.scalar(select(func.count(Interaction.id)))
        vapi_count = await db.scalar(select(func.count(VAPICall.id)))
        token_count = await db.scalar(select(func.count(TokenUsage.id)))
        
        print("\n" + "=" * 70)
        print("📊 VERITABANI DOĞRULAMA RAPORU")
        print("=" * 70)
        print(f"\n✅ Tenants: {tenant_count}")
        print(f"✅ Customers: {customer_count}")
        print(f"✅ Interactions: {interaction_count}")
        print(f"✅ VAPI Calls: {vapi_count}")
        print(f"✅ Token Usage: {token_count}")
        
        total = tenant_count + customer_count + interaction_count + vapi_count + token_count
        print(f"\n📈 Toplam Kayıt: {total}")
        
        # Sample customers
        print("\n" + "=" * 70)
        print("👥 ÖRNEK MÜŞTERİLER (İlk 5)")
        print("=" * 70)
        result = await db.execute(select(Customer).limit(5))
        customers = result.scalars().all()
        
        for c in customers:
            print(f"\n  🔹 {c.customer_id}")
            print(f"     İsim: {c.first_name} {c.last_name}")
            print(f"     Email: {c.email}")
            print(f"     Segment: {c.segment}")
            print(f"     Toplam Harcama: ₺{c.total_spent:.2f}")
        
        # Sample interactions
        print("\n" + "=" * 70)
        print("📅 ÖRNEK ETKİLEŞİMLER (İlk 3)")
        print("=" * 70)
        result = await db.execute(select(Interaction).limit(3))
        interactions = result.scalars().all()
        
        for i in interactions:
            print(f"\n  📌 {i.title}")
            print(f"     Müşteri: {i.client_name}")
            print(f"     Başlangıç: {i.start_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"     Durum: {i.status}")
        
        # Sample VAPI calls
        print("\n" + "=" * 70)
        print("📞 ÖRNEK VAPI ARAMALARI (İlk 3)")
        print("=" * 70)
        result = await db.execute(select(VAPICall).limit(3))
        calls = result.scalars().all()
        
        for call in calls:
            print(f"\n  ☎️  Call ID: {str(call.id)[:8]}...")
            print(f"     Durum: {call.call_status}")
            print(f"     Süre: {call.call_duration_seconds}s")
            print(f"     Duygu: {call.sentiment} ({call.sentiment_score})")
        
        print("\n" + "=" * 70)
        print("✅ DOĞRULAMA TAMAMLANDI!")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify())
