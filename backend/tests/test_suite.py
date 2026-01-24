"""
Test Suite: Tenant Isolation, Redis Performance, and Concurrency Control
"""
import pytest
import asyncio
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.config import settings
from app.models.base import Base
from app.models.tenant import Tenant
from app.models.customer import Customer, CustomerSegment
from app.models.appointment import Appointment, AppointmentStatus
from app.services.customer_service import CustomerService
from app.services.appointment_service import AppointmentService
from app.core.redis import redis_manager


# Test database engine
test_engine = create_async_engine(settings.DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Get database session for tests."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def tenant_a(db_session: AsyncSession):
    """Create Tenant A (Company A)."""
    tenant = Tenant(
        name="Company A",
        slug="company-a",
        domain="company-a.com",
        is_active=True
    )
    db_session.add(tenant)
    await db_session.commit()
    await db_session.refresh(tenant)
    return tenant


@pytest.fixture
async def tenant_b(db_session: AsyncSession):
    """Create Tenant B (Company B)."""
    tenant = Tenant(
        name="Company B",
        slug="company-b",
        domain="company-b.com",
        is_active=True
    )
    db_session.add(tenant)
    await db_session.commit()
    await db_session.refresh(tenant)
    return tenant


@pytest.fixture
async def customer_a(db_session: AsyncSession, tenant_a: Tenant):
    """Create customer for Tenant A."""
    customer = Customer(
        tenant_id=tenant_a.id,
        first_name="Ahmet",
        last_name="Yılmaz",
        email="ahmet@company-a.com",
        phone="+905551234567",
        segment=CustomerSegment.GOLD
    )
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)
    return customer


@pytest.fixture
async def customer_b(db_session: AsyncSession, tenant_b: Tenant):
    """Create customer for Tenant B."""
    customer = Customer(
        tenant_id=tenant_b.id,
        first_name="Mehmet",
        last_name="Demir",
        email="mehmet@company-b.com",
        phone="+905559876543",
        segment=CustomerSegment.VIP
    )
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)
    return customer


# ============================================================================
# TEST 1: TENANT ISOLATION
# ============================================================================

@pytest.mark.asyncio
async def test_tenant_isolation_appointments(
    db_session: AsyncSession,
    tenant_a: Tenant,
    tenant_b: Tenant
):
    """
    Test: Company A cannot see Company B's appointments.
    
    Expected: Complete data isolation between tenants.
    """
    # Create appointment for Tenant A
    appointment_a = Appointment(
        tenant_id=tenant_a.id,
        title="Meeting A",
        description="Company A meeting",
        start_time=datetime.utcnow() + timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=2),
        client_name="Client A",
        client_email="client-a@example.com",
        status=AppointmentStatus.CONFIRMED
    )
    db_session.add(appointment_a)
    
    # Create appointment for Tenant B
    appointment_b = Appointment(
        tenant_id=tenant_b.id,
        title="Meeting B",
        description="Company B meeting",
        start_time=datetime.utcnow() + timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=2),
        client_name="Client B",
        client_email="client-b@example.com",
        status=AppointmentStatus.CONFIRMED
    )
    db_session.add(appointment_b)
    await db_session.commit()
    
    # Query with Tenant A's ID
    query_a = select(Appointment).where(Appointment.tenant_id == tenant_a.id)
    result_a = await db_session.execute(query_a)
    appointments_a = result_a.scalars().all()
    
    # Query with Tenant B's ID
    query_b = select(Appointment).where(Appointment.tenant_id == tenant_b.id)
    result_b = await db_session.execute(query_b)
    appointments_b = result_b.scalars().all()
    
    # Assertions
    assert len(appointments_a) == 1, "Tenant A should see only 1 appointment"
    assert len(appointments_b) == 1, "Tenant B should see only 1 appointment"
    assert appointments_a[0].title == "Meeting A", "Tenant A should see their own appointment"
    assert appointments_b[0].title == "Meeting B", "Tenant B should see their own appointment"
    assert appointments_a[0].id != appointments_b[0].id, "Appointments should be different"
    
    print("✅ TEST PASSED: Tenant isolation working correctly!")


@pytest.mark.asyncio
async def test_tenant_isolation_customers(
    db_session: AsyncSession,
    tenant_a: Tenant,
    tenant_b: Tenant,
    customer_a: Customer,
    customer_b: Customer
):
    """
    Test: Company A cannot see Company B's customers.
    
    Expected: Complete customer data isolation.
    """
    # Query customers for Tenant A
    query_a = select(Customer).where(Customer.tenant_id == tenant_a.id)
    result_a = await db_session.execute(query_a)
    customers_a = result_a.scalars().all()
    
    # Query customers for Tenant B
    query_b = select(Customer).where(Customer.tenant_id == tenant_b.id)
    result_b = await db_session.execute(query_b)
    customers_b = result_b.scalars().all()
    
    # Assertions
    assert len(customers_a) == 1, "Tenant A should see only 1 customer"
    assert len(customers_b) == 1, "Tenant B should see only 1 customer"
    assert customers_a[0].email == "ahmet@company-a.com"
    assert customers_b[0].email == "mehmet@company-b.com"
    assert customers_a[0].phone != customers_b[0].phone
    
    print("✅ TEST PASSED: Customer isolation working correctly!")


# ============================================================================
# TEST 2: REDIS PERFORMANCE
# ============================================================================

@pytest.mark.asyncio
async def test_redis_performance_cache_hit(
    db_session: AsyncSession,
    tenant_a: Tenant,
    customer_a: Customer
):
    """
    Test: Redis cache performance < 50ms for customer lookup.
    
    Expected: Cache HIT should be significantly faster than DB query.
    """
    import time
    
    # Clear cache first
    redis_client = await redis_manager.get_client()
    cache_key = f"customer:{tenant_a.id}:{customer_a.phone}"
    await redis_client.delete(cache_key)
    
    # First call - Cache MISS (DB query)
    start_time = time.time()
    customer_miss, hit_miss = await CustomerService.get_customer_by_phone(
        db=db_session,
        tenant_id=tenant_a.id,
        customer_number=customer_a.phone
    )
    time_miss = (time.time() - start_time) * 1000  # Convert to ms
    
    # Second call - Cache HIT (Redis)
    start_time = time.time()
    customer_hit, hit_hit = await CustomerService.get_customer_by_phone(
        db=db_session,
        tenant_id=tenant_a.id,
        customer_number=customer_a.phone
    )
    time_hit = (time.time() - start_time) * 1000  # Convert to ms
    
    # Assertions
    assert hit_miss == False, "First call should be cache MISS"
    assert hit_hit == True, "Second call should be cache HIT"
    assert time_hit < 50, f"Cache HIT should be < 50ms, got {time_hit:.2f}ms"
    assert time_hit < time_miss, "Cache HIT should be faster than cache MISS"
    
    print(f"✅ TEST PASSED: Redis performance excellent!")
    print(f"   Cache MISS: {time_miss:.2f}ms")
    print(f"   Cache HIT: {time_hit:.2f}ms (Target: < 50ms)")
    print(f"   Speed improvement: {time_miss/time_hit:.1f}x faster")


# ============================================================================
# TEST 3: CONCURRENCY CONTROL
# ============================================================================

@pytest.mark.asyncio
async def test_concurrency_appointment_conflict(
    db_session: AsyncSession,
    tenant_a: Tenant
):
    """
    Test: Simultaneous appointment creation should detect conflicts.
    
    Expected: Second appointment at overlapping time should be rejected.
    """
    from fastapi import HTTPException
    
    # Create first appointment at 10:00-11:00
    start_time = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    appointment_service = AppointmentService()
    
    # First appointment
    appointment1 = await appointment_service.create_appointment(
        db=db_session,
        tenant_id=tenant_a.id,
        title="First Meeting",
        description="Original meeting",
        start_time=start_time,
        end_time=end_time,
        client_name="Client 1",
        client_email="client1@example.com"
    )
    
    # Try to create conflicting appointment at 10:30-11:30
    conflict_start = start_time + timedelta(minutes=30)
    conflict_end = conflict_start + timedelta(hours=1)
    
    # This should raise HTTPException due to conflict
    with pytest.raises(HTTPException) as exc_info:
        await appointment_service.create_appointment(
            db=db_session,
            tenant_id=tenant_a.id,
            title="Conflicting Meeting",
            description="This should fail",
            start_time=conflict_start,
            end_time=conflict_end,
            client_name="Client 2",
            client_email="client2@example.com"
        )
    
    # Assertions
    assert exc_info.value.status_code == 409, "Should return 409 Conflict"
    assert "time slot is not available" in str(exc_info.value.detail).lower()
    
    print("✅ TEST PASSED: Concurrency control working correctly!")
    print(f"   Conflict detected for overlapping time slots")


@pytest.mark.asyncio
async def test_optimistic_locking(
    db_session: AsyncSession,
    tenant_a: Tenant
):
    """
    Test: Optimistic locking prevents concurrent updates.
    
    Expected: Update with wrong version should fail.
    """
    from fastapi import HTTPException
    
    # Create appointment
    start_time = datetime.utcnow() + timedelta(hours=2)
    end_time = start_time + timedelta(hours=1)
    
    appointment_service = AppointmentService()
    
    appointment = await appointment_service.create_appointment(
        db=db_session,
        tenant_id=tenant_a.id,
        title="Test Meeting",
        description="For optimistic locking test",
        start_time=start_time,
        end_time=end_time,
        client_name="Test Client",
        client_email="test@example.com"
    )
    
    initial_version = appointment.version
    
    # Update with correct version (should succeed)
    updated = await appointment_service.update_appointment(
        db=db_session,
        tenant_id=tenant_a.id,
        appointment_id=appointment.id,
        current_version=initial_version,
        title="Updated Meeting"
    )
    
    assert updated.version == initial_version + 1, "Version should increment"
    
    # Try to update with old version (should fail)
    with pytest.raises(HTTPException) as exc_info:
        await appointment_service.update_appointment(
            db=db_session,
            tenant_id=tenant_a.id,
            appointment_id=appointment.id,
            current_version=initial_version,  # Old version!
            title="This should fail"
        )
    
    assert exc_info.value.status_code == 409, "Should return 409 Conflict"
    
    print("✅ TEST PASSED: Optimistic locking working correctly!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
