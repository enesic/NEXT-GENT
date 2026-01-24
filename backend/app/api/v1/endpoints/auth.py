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
    email: EmailStr
    password: str
    tenant_id: Optional[str] = None  # Optional tenant slug or ID


class LoginResponse(BaseModel):
    token: str
    user: dict
    tenant_id: str
    sector: str
    tenant_name: str


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
    Login endpoint with automatic sector detection.
    """
    # Step 1: Detect sector
    sector_info = await detect_sector(
        SectorDetectionRequest(
            email=request.email,
            tenant_id=request.tenant_id
        ),
        db=db
    )
    
    # Step 2: Authenticate (simplified - in production, use proper auth)
    # For now, accept any email/password combination
    # In production, verify password hash
    
    # Step 3: Generate token (simplified)
    import secrets
    token = f"token_{secrets.token_urlsafe(32)}"
    
    # Step 4: Get or create user
    user = {
        "id": 1,
        "email": request.email,
        "name": request.email.split('@')[0].replace('.', ' ').title()
    }
    
    logger.info(
        "user_login",
        email=request.email,
        sector=sector_info.sector,
        tenant_id=sector_info.tenant_id,
        confidence=sector_info.confidence
    )
    
    return LoginResponse(
        token=token,
        user=user,
        tenant_id=sector_info.tenant_id,
        sector=sector_info.sector,
        tenant_name=sector_info.tenant_name
    )

