#!/usr/bin/env python3
"""
Update database schema for analytics and call center data
"""
import asyncio
import asyncpg

DATABASE_URL = "postgresql://neondb_owner:npg_leRNYA8SMiK9@ep-silent-water-ai73m23k-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def update_schema():
    """Update schema for analytics support"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Updating database schema for analytics...")
        
        # Create call_interactions table for analytics
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS call_interactions (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id),
            customer_id INTEGER REFERENCES customers(id),
            interaction_type VARCHAR(50) NOT NULL,
            call_duration_seconds INTEGER DEFAULT 0,
            satisfaction_score INTEGER CHECK (satisfaction_score >= 1 AND satisfaction_score <= 5),
            resolution_status VARCHAR(50) DEFAULT 'pending',
            agent_name VARCHAR(100),
            call_timestamp TIMESTAMPTZ DEFAULT NOW(),
            call_summary TEXT,
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create indexes for performance
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_call_interactions_tenant ON call_interactions(tenant_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_call_interactions_customer ON call_interactions(customer_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_call_interactions_timestamp ON call_interactions(call_timestamp);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_call_interactions_type ON call_interactions(interaction_type);")
        
        # Create analytics_metrics table for dashboard KPIs
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS analytics_metrics (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id),
            metric_name VARCHAR(100) NOT NULL,
            metric_value NUMERIC(15,2),
            metric_date DATE DEFAULT CURRENT_DATE,
            metric_period VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create unique constraint for metrics
        await conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_analytics_unique 
        ON analytics_metrics(tenant_id, metric_name, metric_date, metric_period);
        """)
        
        # Create token_usage table for API tracking
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS token_usage (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id),
            usage_type VARCHAR(50) NOT NULL, -- 'api_call', 'ai_tokens', 'storage'
            usage_amount INTEGER DEFAULT 0,
            usage_date DATE DEFAULT CURRENT_DATE,
            endpoint VARCHAR(100),
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        
        # Create indexes for token usage
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_token_usage_tenant_date ON token_usage(tenant_id, usage_date);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_token_usage_type ON token_usage(usage_type);")
        
        print("Schema update completed!")
        
    except Exception as e:
        print(f"Schema update error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(update_schema())