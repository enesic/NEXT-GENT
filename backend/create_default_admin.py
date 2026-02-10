"""
Create default admin user for NextGent system (non-interactive).
This script creates a default admin with predefined credentials for demo purposes.
"""
import asyncio
import os
import sys
import bcrypt
from sqlalchemy import select

# Ensure we can import app modules
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.admin_user import AdminUser, AdminRole


async def create_default_admin():
    """Create a default admin user with predefined credentials"""
    print("\n🔐 Creating default admin user...")
    
    async with AsyncSessionLocal() as db:
        # Check if any admin already exists
        result = await db.execute(select(AdminUser))
        existing_admin = result.scalars().first()
        
        if existing_admin:
            print(f"✅ Admin user already exists: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Role: {existing_admin.role}")
            return
        
        # Default credentials for demo
        username = "admin"
        email = "admin@nextgent.com"
        password = "admin123"  # Simple password for demo
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create admin user
        admin = AdminUser(
            username=username,
            email=email,
            password_hash=password_hash,
            role=AdminRole.SUPER_ADMIN,
            is_active=True,
            is_super_admin=True,
            permissions={
                "users": ["create", "read", "update", "delete", "anonymize"],
                "logs": ["read", "export"],
                "analytics": ["read", "export"],
                "settings": ["read", "update"],
                "admin_users": ["create", "read", "update", "delete"]
            }
        )
        
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        
        print("✅ Default admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Role: {AdminRole.SUPER_ADMIN}")
        print("\n⚠️  Remember to change the password after first login!")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(create_default_admin())
