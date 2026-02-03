import asyncio
import asyncpg
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def audit_users():
    conn = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='nextgent',
        host='localhost',
        port=5432
    )

    print("\n--- NEXTGENT DB AUDIT ---\n")
    
    # List Tables
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    print("Tables found:", [t['table_name'] for t in tables])

    # Check tenants
    try:
        tenants = await conn.fetch("SELECT id, name, is_active FROM tenants")
        print(f"\nTotal Tenants: {len(tenants)}")
        for t in tenants:
            print(f"Tenant: {t['name']} (ID: {t['id']}) Active: {t['is_active']}")
    except Exception as e:
        print(f"Error querying tenants: {e}")

    # Check customers (Used for Login!)
    try:
        customers = await conn.fetch("""
            SELECT customer_id, first_name, last_name, email, segment::text, status::text 
            FROM customers
        """)
        print(f"\nTotal Customers (Logins): {len(customers)}")
        
        for c in customers:
            print(f"User ID: {c['customer_id']} | Name: {c['first_name']} {c['last_name']} | Email: {c['email']} | Segment: {c['segment']} | Active: {c['status']}")
            
    except Exception as e:
        print(f"Error querying customers: {e}") 
        
    await conn.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(audit_users())
