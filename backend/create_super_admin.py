"""
Create super admin user for the NextGent system.
This script creates a super admin with full permissions.
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


async def create_super_admin():
    """Create a super admin user with full permissions"""
    print("=" * 60)
    print("Creating Super Admin User for NextGent")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Check if super admin already exists
        result = await db.execute(
            select(AdminUser).where(AdminUser.is_super_admin == True)
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print(f"\n⚠️  Super admin already exists: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            print("\nTo reset password, delete the existing admin from database first.")
            return
        
        # Get username and password
        print("\n📝 Enter admin credentials:")
        username = input("Username (default: admin): ").strip() or "admin"
        email = input("Email (default: admin@nextgent.com): ").strip() or "admin@nextgent.com"
        
        # Generate strong password
        import secrets
        import string
        
        # Generate a secure random password
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(16))
        
        print(f"\n🔐 Generated secure password: {password}")
        print("⚠️  SAVE THIS PASSWORD - It will NOT be shown again!")
        
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
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Super Admin Created")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Role: {AdminRole.SUPER_ADMIN}")
        print("\n⚠️  Important:")
        print("1. Save these credentials in a secure location")
        print("2. Change the password after first login")
        print("3. Enable 2FA for additional security")
        print("\n🚀 You can now login to the admin panel!")
        print("=" * 60)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(create_super_admin())
