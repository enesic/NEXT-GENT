"""
Production bootstrap script.

Creates missing tables and ensures minimum required records exist:
- one active tenant
- one admin user (admin/admin123) if none exists
- one demo customer (BEA-000001 / 1234) if missing
"""
import asyncio
import bcrypt
from sqlalchemy import select, text

from app.core.database import engine, AsyncSessionLocal
from app.models.base import Base
import app.models  # noqa: F401 - ensures all models are registered
from app.models.tenant import Tenant
from app.models.admin_user import AdminUser, AdminRole
from app.models.customer import Customer, CustomerSegment, CustomerStatus


DEFAULT_TENANT_SLUG = "nextgent-main"
DEFAULT_TENANT_NAME = "NextGent Main"
DEFAULT_CUSTOMER_ID = "BEA-000001"
DEFAULT_CUSTOMER_PIN = "1234"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


async def ensure_schema() -> None:
    if engine is None:
        raise RuntimeError("Database engine is not configured")

    async with engine.begin() as conn:
        # Backfill legacy production schemas where tables exist but columns are missing.
        # create_all does not alter existing tables.
        await conn.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'customer_segment') THEN
                        CREATE TYPE customer_segment AS ENUM ('vip', 'gold', 'silver', 'bronze', 'regular');
                    END IF;
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'customer_status') THEN
                        CREATE TYPE customer_status AS ENUM ('active', 'inactive', 'blocked', 'debt');
                    END IF;
                END$$;
                """
            )
        )
        await conn.execute(text("ALTER TABLE IF EXISTS tenants ADD COLUMN IF NOT EXISTS config JSONB"))
        await conn.execute(text("ALTER TABLE IF EXISTS tenants ADD COLUMN IF NOT EXISTS webhook_url VARCHAR"))
        await conn.execute(text("ALTER TABLE IF EXISTS tenants ADD COLUMN IF NOT EXISTS system_prompt VARCHAR"))
        await conn.execute(text("ALTER TABLE IF EXISTS tenants ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
        await conn.execute(text("ALTER TABLE IF EXISTS tenants ADD COLUMN IF NOT EXISTS domain VARCHAR"))

        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS customer_id VARCHAR(20)"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS pin_hash VARCHAR(255)"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS phone_hash VARCHAR(64)"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS segment customer_segment DEFAULT 'regular'"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS status customer_status DEFAULT 'active'"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS total_orders INTEGER DEFAULT 0"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS total_spent NUMERIC(10,2) DEFAULT 0"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS lifetime_value NUMERIC(10,2) DEFAULT 0"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS debt_amount NUMERIC(10,2) DEFAULT 0"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS last_order_date TIMESTAMP"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS last_contact_date TIMESTAMP"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS referral_code VARCHAR(50)"))
        await conn.execute(text("ALTER TABLE IF EXISTS customers ADD COLUMN IF NOT EXISTS referred_by VARCHAR(50)"))

        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'admin'"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS is_super_admin BOOLEAN DEFAULT FALSE"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS permissions JSONB"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMPTZ"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS login_count INTEGER DEFAULT 0"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS last_ip VARCHAR"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS two_factor_secret VARCHAR"))
        await conn.execute(text("ALTER TABLE IF EXISTS admin_users ADD COLUMN IF NOT EXISTS two_factor_enabled BOOLEAN DEFAULT FALSE"))

        await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS customers_customer_id_key ON customers (customer_id)"))
        await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS customers_phone_hash_key ON customers (phone_hash)"))
        await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS admin_users_username_key ON admin_users (username)"))
        await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS admin_users_email_key ON admin_users (email)"))

        await conn.run_sync(Base.metadata.create_all)


async def ensure_tenant(db) -> Tenant:
    result = await db.execute(select(Tenant).where(Tenant.slug == DEFAULT_TENANT_SLUG))
    tenant = result.scalar_one_or_none()
    if tenant:
        return tenant

    tenant = Tenant(
        name=DEFAULT_TENANT_NAME,
        slug=DEFAULT_TENANT_SLUG,
        domain="nextgent.co",
        is_active=True,
        config={"sector": "beauty"},
    )
    db.add(tenant)
    await db.flush()
    return tenant


async def ensure_admin(db) -> None:
    result = await db.execute(select(AdminUser).limit(1))
    existing = result.scalar_one_or_none()
    if existing:
        return

    password_hash = bcrypt.hashpw(
        DEFAULT_ADMIN_PASSWORD.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    admin = AdminUser(
        username=DEFAULT_ADMIN_USERNAME,
        email="info@nextgent.co",
        password_hash=password_hash,
        role=AdminRole.SUPER_ADMIN,
        is_active=True,
        is_super_admin=True,
        permissions={
            "users": ["create", "read", "update", "delete", "anonymize"],
            "logs": ["read", "export"],
            "analytics": ["read", "export"],
            "settings": ["read", "update"],
            "admin_users": ["create", "read", "update", "delete"],
        },
    )
    db.add(admin)


async def ensure_demo_customer(db, tenant: Tenant) -> None:
    result = await db.execute(
        select(Customer).where(Customer.customer_id == DEFAULT_CUSTOMER_ID)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return

    pin_hash = bcrypt.hashpw(
        DEFAULT_CUSTOMER_PIN.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    customer = Customer(
        tenant_id=tenant.id,
        customer_id=DEFAULT_CUSTOMER_ID,
        first_name="NextGent",
        last_name="Demo",
        email="info@nextgent.co",
        pin_hash=pin_hash,
        segment=CustomerSegment.REGULAR,
        status=CustomerStatus.ACTIVE,
    )
    customer.set_phone("+905551112233")
    db.add(customer)


async def bootstrap() -> None:
    await ensure_schema()

    async with AsyncSessionLocal() as db:
        tenant = await ensure_tenant(db)
        await ensure_admin(db)
        await ensure_demo_customer(db, tenant)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(bootstrap())
