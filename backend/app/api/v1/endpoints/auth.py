"""
Authentication and sector detection endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.logger import get_logger
from app.models.tenant import Tenant
from app.models.customer import Customer

router = APIRouter()
logger = get_logger(__name__)


class LoginRequest(BaseModel):
    customer_id: str  # Format: SECTOR-NNNNNN (e.g., MED-001234)
    pin: str          # 4-6 digit PIN or password
    tenant_id: Optional[str] = None  # Optional tenant slug or ID


class LoginResponse(BaseModel):
    token: str
    user: dict
    tenant_id: str
    sector: str
    tenant_name: str
    customer_id: str  # Return customer_id for frontend


class SectorDetectionRequest(BaseModel):
    email: EmailStr
    tenant_id: Optional[str] = None


class SectorDetectionResponse(BaseModel):
    sector: str
    tenant_id: str
    tenant_name: str
    confidence: float  # 0.0 - 1.0


@router.post("/detect-sector", response_model=SectorDetectionResponse)
async def detect_sector(
    request: SectorDetectionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Automatically detect sector based on email domain or tenant information.
    
    Strategy:
    1. If tenant_id provided, get sector from tenant config
    2. If email domain matches known patterns, detect sector
    3. If customer exists, get sector from customer's tenant
    4. Default to 'medical' if no match
    """
    sector = None
    tenant_id = None
    tenant_name = None
    confidence = 0.0
    
    # Strategy 1: Tenant ID provided
    if request.tenant_id:
        try:
            # Try as UUID first
            from uuid import UUID
            tenant_uuid = UUID(request.tenant_id)
            query = select(Tenant).where(Tenant.id == tenant_uuid)
        except ValueError:
            # Try as slug
            query = select(Tenant).where(Tenant.slug == request.tenant_id)
        
        result = await db.execute(query)
        tenant = result.scalar_one_or_none()
        
        if tenant:
            sector = tenant.config.get('sector') if tenant.config else 'medical'
            tenant_id = str(tenant.id)
            tenant_name = tenant.name
            confidence = 1.0
            logger.info("sector_detected_from_tenant", tenant_id=tenant_id, sector=sector)
    
    # Strategy 2: Email domain pattern matching
    if not sector:
        email_domain = request.email.split('@')[1].lower()
        
        # Known domain patterns
        medical_domains = ['hospital', 'clinic', 'health', 'medical', 'doctor', 'doktor', 'saglik']
        legal_domains = ['law', 'legal', 'avukat', 'hukuk', 'lawyer', 'attorney']
        real_estate_domains = ['realty', 'estate', 'property', 'emlak', 'gayrimenkul', 'konut']
        
        if any(pattern in email_domain for pattern in medical_domains):
            sector = 'medical'
            confidence = 0.8
        elif any(pattern in email_domain for pattern in legal_domains):
            sector = 'legal'
            confidence = 0.8
        elif any(pattern in email_domain for pattern in real_estate_domains):
            sector = 'real_estate'
            confidence = 0.8
    
    # Strategy 3: Find customer by email
    if not sector or confidence < 0.9:
        query = select(Customer).where(Customer.email == request.email)
        result = await db.execute(query)
        customer = result.scalar_one_or_none()
        
        if customer:
            # Get tenant from customer
            tenant_query = select(Tenant).where(Tenant.id == customer.tenant_id)
            tenant_result = await db.execute(tenant_query)
            tenant = tenant_result.scalar_one_or_none()
            
            if tenant:
                sector = tenant.config.get('sector') if tenant.config else 'medical'
                tenant_id = str(tenant.id)
                tenant_name = tenant.name
                confidence = 0.9
                logger.info("sector_detected_from_customer", email=request.email, sector=sector)
    
    # Strategy 4: Default fallback
    if not sector:
        sector = 'medical'
        confidence = 0.5
        logger.warning("sector_detection_fallback", email=request.email, default_sector=sector)
    
    # If tenant_id still not found, create or find default tenant
    if not tenant_id:
        try:
            # Try to find a tenant with matching sector
            # We fetch potential candidates and filter in Python to avoid DB-specific JSON syntax issues if possible,
            # or strictly use the PG syntax if we are sure. To be safe against "None" configs:
            query = select(Tenant).where(Tenant.config.is_not(None))
            result = await db.execute(query)
            tenants = result.scalars().all()
            
            # Filter in python for safety and robustness
            matching_tenant = next(
                (t for t in tenants if t.config.get('sector') == sector), 
                None
            )
            
            if matching_tenant:
                tenant_id = str(matching_tenant.id)
                tenant_name = matching_tenant.name
            else:
                # Create a default tenant placeholder (with valid UUID format)
                # This prevents "invalid uuid" errors in frontend/backend validation
                tenant_id = "00000000-0000-0000-0000-000000000000"
                tenant_name = f"Default {sector.title()} Tenant"
                logger.warning("no_tenant_found", sector=sector, created_default=True)
                
        except Exception as e:
            # Fallback
            logger.error("tenant_query_error", error=str(e))
            tenant_id = "00000000-0000-0000-0000-000000000000"
            tenant_name = f"Default {sector.title()} Tenant"
    
    return SectorDetectionResponse(
        sector=sector,
        tenant_id=tenant_id,
        tenant_name=tenant_name,
        confidence=confidence
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint with customer ID + PIN authentication.
    
    Customer ID Format: SECTOR-NNNNNN
    Examples: MED-001234, LEG-005678, MFG-009999
    """
    import bcrypt
    
    # Step 1: Find customer by customer_id
    query = select(Customer).where(Customer.customer_id == request.customer_id.upper())
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    
    if not customer:
        # Customer ID not found
        raise HTTPException(
            status_code=401,
            detail="Invalid customer ID or PIN"
        )
    
    # Step 2: Verify PIN
    if customer.pin_hash:
        # Verify bcrypt hash
        pin_valid = bcrypt.checkpw(
            request.pin.encode('utf-8'),
            customer.pin_hash.encode('utf-8')
        )
        
        if not pin_valid:
            # Wrong PIN
            raise HTTPException(
                status_code=401,
                detail="Invalid customer ID or PIN"
            )
    else:
        # No PIN set (should not happen in production)
        raise HTTPException(
            status_code=401,
            detail="Account not configured. Please contact support."
        )
    
    # Step 3: Get tenant and sector
    tenant_query = select(Tenant).where(Tenant.id == customer.tenant_id)
    tenant_result = await db.execute(tenant_query)
    tenant = tenant_result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=500,
            detail="Tenant configuration error"
        )
    
    sector = tenant.config.get('sector') if tenant.config else 'medical'
    
    # Step 4: Generate token
    import secrets
    token = f"token_{secrets.token_urlsafe(32)}"
    
    # Step 5: Build user object
    user = {
        "id": str(customer.id),
        "customer_id": customer.customer_id,
        "name": f"{customer.first_name} {customer.last_name}",
        "email": customer.email,
        "phone": customer.phone,
        "segment": customer.segment.value if customer.segment else "regular"
    }
    
    logger.info(
        "customer_login",
        customer_id=customer.customer_id,
        sector=sector,
        tenant_id=str(tenant.id)
    )
    
    return LoginResponse(
        token=token,
        user=user,
        tenant_id=str(tenant.id),
        sector=sector,
        tenant_name=tenant.name,
        customer_id=customer.customer_id
    )

