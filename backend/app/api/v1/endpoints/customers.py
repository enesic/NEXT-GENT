from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.customer import CustomerSegment, CustomerStatus
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerStatusCheck,
    CustomerSegmentationResult
)
from app.services.customer_service import CustomerService

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    customer_in: CustomerCreate,
):
    """
    Create a new customer.
    """
    customer = await CustomerService.create_customer(
        db=db,
        tenant_id=current_tenant.id,
        customer_data=customer_in
    )
    return customer


@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    segment: Optional[CustomerSegment] = Query(None, description="Filter by segment"),
    status: Optional[CustomerStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List customers with optional filters.
    """
    customers = await CustomerService.list_customers(
        db=db,
        tenant_id=current_tenant.id,
        segment=segment,
        status=status,
        skip=skip,
        limit=limit
    )
    return customers


@router.get("/by-phone/{phone}", response_model=CustomerResponse)
async def get_customer_by_phone(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    phone: str,
    use_cache: bool = Query(True, description="Use Redis cache for faster lookup"),
):
    """
    Get customer by phone number (with Redis caching - Antigravity Speed).
    
    This endpoint demonstrates the caching strategy:
    1. Check Redis cache first
    2. If not found, query PostgreSQL
    3. Cache the result for future requests
    """
    customer = await CustomerService.get_customer_by_phone(
        db=db,
        tenant_id=current_tenant.id,
        phone=phone,
        use_cache=use_cache
    )
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer


@router.get("/check-status/{phone}", response_model=CustomerStatusCheck)
async def check_customer_status(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    phone: str,
):
    """
    Check customer status with complex branching logic.
    
    Returns detailed status including:
    - Segment (VIP, GOLD, etc.)
    - Status (ACTIVE, DEBT, BLOCKED, etc.)
    - Debt information
    - Inactivity status
    - Recommended action
    
    This implements the workflow from the CRM diagram.
    """
    import structlog
    logger = structlog.get_logger(__name__)
    
    # KVKK/GDPR Audit Log
    logger.info(
        "kvkk_audit_access",
        action="check_customer_status",
        phone_masked=f"{phone[:3]}***{phone[-2:]}",
        tenant_id=str(current_tenant.id),
        compliance="KVKK_DATA_PROCESSED"
    )

    status_check = await CustomerService.check_customer_status(
        db=db,
        tenant_id=current_tenant.id,
        phone=phone
    )
    return status_check


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    customer_id: UUID,
):
    """
    Get a specific customer by ID.
    """
    from sqlalchemy import select, and_
    from app.models.customer import Customer
    
    query = select(Customer).where(
        and_(
            Customer.id == customer_id,
            Customer.tenant_id == current_tenant.id
        )
    )
    
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    customer_id: UUID,
    customer_in: CustomerUpdate,
):
    """
    Update a customer.
    
    Note: Cache will be automatically invalidated.
    """
    customer = await CustomerService.update_customer(
        db=db,
        tenant_id=current_tenant.id,
        customer_id=customer_id,
        customer_data=customer_in
    )
    return customer


@router.post("/{customer_id}/segment", response_model=CustomerSegmentationResult)
async def segment_customer(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    customer_id: UUID,
):
    """
    Manually trigger customer segmentation.
    
    Automatically calculates and updates customer segment based on:
    - Total spent
    - Total orders
    - Lifetime value
    
    Segmentation rules:
    - VIP: $10,000+ spent OR 50+ orders
    - GOLD: $5,000+ spent OR 25+ orders
    - SILVER: $1,000+ spent OR 10+ orders
    - BRONZE: $500+ spent OR 5+ orders
    - REGULAR: Default
    """
    from sqlalchemy import select, and_
    from app.models.customer import Customer
    
    query = select(Customer).where(
        and_(
            Customer.id == customer_id,
            Customer.tenant_id == current_tenant.id
        )
    )
    
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    segmentation_result = await CustomerService.segment_customer(db, customer)
    return segmentation_result


@router.post("/{customer_id}/update-stats", response_model=CustomerResponse)
async def update_customer_stats(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    customer_id: UUID,
    order_amount: float = Query(..., description="Order amount to add to customer stats"),
):
    """
    Update customer statistics after an order.
    
    This will:
    1. Increment total_orders
    2. Add to total_spent and lifetime_value
    3. Update last_order_date
    4. Automatically re-segment customer if needed
    5. Invalidate cache
    """
    customer = await CustomerService.update_customer_stats(
        db=db,
        customer_id=customer_id,
        order_amount=order_amount
    )
    return customer
