#!/usr/bin/env python3
"""
Migrate database schema to Neon.tech
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv('.env.production')

async def migrate():
    conn_str = os.getenv('DATABASE_URL')
    conn = await asyncpg.connect(conn_str)
    
    try:
        # Create enum types
        await conn.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'customer_segment') THEN
                CREATE TYPE customer_segment AS ENUM ('vip', 'gold', 'silver', 'bronze', 'regular');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'customer_status') THEN
                CREATE TYPE customer_status AS ENUM ('active', 'inactive', 'blocked', 'debt');
            END IF;
        END$$;
        """)
        
        # Create tenants table
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            domain VARCHAR(255),
            config JSONB DEFAULT '{}',
            webhook_url VARCHAR(500),
            system_prompt TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create admin_users table
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'admin',
            is_active BOOLEAN DEFAULT TRUE,
            is_super_admin BOOLEAN DEFAULT FALSE,
            permissions JSONB DEFAULT '{}',
            last_login_at TIMESTAMPTZ,
            login_count INTEGER DEFAULT 0,
            last_ip VARCHAR(45),
            two_factor_secret VARCHAR(32),
            two_factor_enabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create customers table
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id),
            customer_id VARCHAR(20) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255),
            pin_hash VARCHAR(255) NOT NULL,
            phone_hash VARCHAR(64) UNIQUE,
            segment customer_segment DEFAULT 'regular',
            status customer_status DEFAULT 'active',
            total_orders INTEGER DEFAULT 0,
            total_spent NUMERIC(10,2) DEFAULT 0,
            lifetime_value NUMERIC(10,2) DEFAULT 0,
            debt_amount NUMERIC(10,2) DEFAULT 0,
            last_order_date TIMESTAMP,
            last_contact_date TIMESTAMP,
            referral_code VARCHAR(50),
            referred_by VARCHAR(50),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create sample data
        # Insert default tenant
        await conn.execute("""
        INSERT INTO tenants (name, slug, domain, is_active, config)
        VALUES ('NextGent Main', 'nextgent-main', 'nextgent.co', TRUE, '{"sector": "beauty"}')
        ON CONFLICT (slug) DO NOTHING;
        """)
        
        # Insert admin user (admin/admin123)
        await conn.execute("""
        INSERT INTO admin_users (username, email, password_hash, role, is_active, is_super_admin, permissions)
        VALUES (
            'admin', 
            'info@nextgent.co',
            '$2b$12$6Tc.8Z9yLQJ5ELjHHdVfaOa8eZHjQ3z1QRjRzv.cMGJJ8BDZ1LQ1.',
            'super_admin',
            TRUE,
            TRUE,
            '{"users": ["create", "read", "update", "delete"], "logs": ["read"], "settings": ["update"]}'
        )
        ON CONFLICT (username) DO NOTHING;
        """)
        
        # Insert demo customer (BEA-000001 / 1234)
        tenant_id = await conn.fetchval("SELECT id FROM tenants WHERE slug = 'nextgent-main'")
        await conn.execute("""
        INSERT INTO customers (tenant_id, customer_id, first_name, last_name, email, pin_hash, segment, status)
        VALUES ($1, 'BEA-000001', 'NextGent', 'Demo', 'info@nextgent.co', '$2b$12$6Tc.8Z9yLQJ5ELjHHdVfaOa8eZHjQ3z1QRjRzv.cMGJJ8BDZ1LQ1.', 'regular', 'active')
        ON CONFLICT (customer_id) DO NOTHING;
        """, tenant_id)
        
        print("SUCCESS: Schema migrated and sample data inserted")
        
    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(migrate())