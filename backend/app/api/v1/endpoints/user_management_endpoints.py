"""
User Management Endpoints for Admin Panel
Includes user creation, updates, password/PIN management, and KVKK compliance
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, or_
from pydantic import BaseModel, EmailStr
import bcrypt

from app.core.database import get_db
from app.core.logger import get_logger
from app.core.pii_masker import pii_masker
from app.models.customer import Customer, CustomerSegment, CustomerStatus
from app.models.admin_user import AdminUser
from app.models.audit_log import AuditLog, ActionType
from app.api.v1.endpoints.auth_endpoints import get_current_admin

router = APIRouter()
logger = get_logger(__name__)


# Schemas
class UserCreateRequest(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    segment: CustomerSegment = "regular"
    pin: str  # 4-digit PIN


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    segment: Optional[CustomerSegment] = None
    status: Optional[CustomerStatus] = None


class PasswordUpdateRequest(BaseModel):
    new_pin: str  # 4-digit PIN
    confirm_pin: str


class UserResponse(BaseModel):
    id: str
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: str  # Will be masked
    segment: str
    status: str
    created_at: str
    updated_at: str


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    page_size: int


# Helper Functions
def hash_pin(pin: str) -> str:
    """Hash PIN using bcrypt"""
    return bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def mask_user_data(user: Customer) -> dict:
    """Mask sensitive user data for display"""
    return {
        "id": str(user.id),
        "customer_id": user.customer_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": pii_masker.mask_email(user.email),
        "phone": pii_masker.mask_phone(user.phone),
        "segment": user.segment.value if hasattr(user.segment, 'value') else user.segment,
        "status": user.status.value if hasattr(user.status, 'value') else user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }


# Endpoints
@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new user.
    Requires admin authentication.
    """
    try:
        # Check if user already exists
        result = await db.execute(
            select(Customer).where(
                or_(
                    Customer.customer_id == user_data.customer_id,
                    Customer.email == user_data.email,
                    Customer.phone == user_data.phone
                )
            )
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this ID, email, or phone already exists"
            )
        
        # Validate PIN
        if len(user_data.pin) != 4 or not user_data.pin.isdigit():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN must be exactly 4 digits"
            )
        
        # Hash PIN
        pin_hash = hash_pin(user_data.pin)
        
        # Create user
        new_user = Customer(
            customer_id=user_data.customer_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            segment=user_data.segment,
            status=CustomerStatus.ACTIVE,
            pin_hash=pin_hash
        )
        
        db.add(new_user)
        await db.flush()
        
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.CREATE,
            resource_type="customer",
            admin_user_id=str(current_admin.id),
            resource_id=str(new_user.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={
                "action": "User created",
                "customer_id": user_data.customer_id,
                "email": user_data.email,
                "phone": user_data.phone
            }
        )
        db.add(audit_log)
        
        await db.commit()
        await db.refresh(new_user)
        
        logger.info("user_created", admin_id=str(current_admin.id), customer_id=user_data.customer_id)
        
        return UserResponse(**mask_user_data(new_user))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("create_user_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/users", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    segment: Optional[CustomerSegment] = None,
    status: Optional[CustomerStatus] = None,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    List all users with pagination and filtering.
    All PII is masked in the response.
    """
    try:
        # Build query
        query = select(Customer)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Customer.customer_id.ilike(search_term),
                    Customer.first_name.ilike(search_term),
                    Customer.last_name.ilike(search_term)
                )
            )
        
        if segment:
            query = query.where(Customer.segment == segment)
            
        if status:
            query = query.where(Customer.status == status)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Mask user data
        masked_users = [UserResponse(**mask_user_data(user)) for user in users]
        
        return UserListResponse(
            users=masked_users,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error("list_users_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    update_data: UserUpdateRequest,
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user information.
    Creates audit log with changes.
    """
    try:
        # Get user
        result = await db.execute(
            select(Customer).where(Customer.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Track changes for audit
        changes_before = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "segment": user.segment.value if hasattr(user.segment, 'value') else user.segment
        }
        
        # Update fields
        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(user, field, value)
        
        changes_after = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "segment": user.segment.value if hasattr(user.segment, 'value') else user.segment
        }
        
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.UPDATE,
            resource_type="customer",
            admin_user_id=str(current_admin.id),
            resource_id=str(user.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={
                "before": changes_before,
                "after": changes_after
            }
        )
        db.add(audit_log)
        
        await db.commit()
        await db.refresh(user)
        
        logger.info("user_updated", admin_id=str(current_admin.id), user_id=user_id)
        
        return UserResponse(**mask_user_data(user))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("update_user_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.post("/users/{user_id}/change-pin")
async def change_user_pin(
    user_id: str,
    pin_data: PasswordUpdateRequest,
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user's PIN.
    Admin can reset user password/PIN for account recovery.
    """
    try:
        # Validate PIN
        if pin_data.new_pin != pin_data.confirm_pin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PINs do not match"
            )
        
        if len(pin_data.new_pin) != 4 or not pin_data.new_pin.isdigit():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN must be exactly 4 digits"
            )
        
        # Get user
        result = await db.execute(
            select(Customer).where(Customer.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update PIN
        user.pin_hash = hash_pin(pin_data.new_pin)
        
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.PASSWORD_CHANGE,
            resource_type="customer",
            admin_user_id=str(current_admin.id),
            resource_id=str(user.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={
                "action": "PIN changed by admin",
                "customer_id": user.customer_id
            }
        )
        db.add(audit_log)
        
        await db.commit()
        
        logger.info("user_pin_changed", admin_id=str(current_admin.id), user_id=user_id)
        
        return {"message": "PIN changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("change_pin_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change PIN"
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user (KVKK compliant hard delete).
    Requires super admin for safety.
    """
    try:
        # Check super admin permission
        if not current_admin.is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super admins can delete users"
            )
        
        # Get user
        result = await db.execute(
            select(Customer).where(Customer.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create audit log before deletion
        audit_log = AuditLog.create_log(
            action_type=ActionType.DELETE,
            resource_type="customer",
            admin_user_id=str(current_admin.id),
            resource_id=str(user.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={
                "action": "User deleted (KVKK)",
                "customer_id": user.customer_id
            }
        )
        db.add(audit_log)
        
        # Hard delete
        await db.delete(user)
        await db.commit()
        
        logger.info("user_deleted", admin_id=str(current_admin.id), user_id=user_id)
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("delete_user_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.post("/users/{user_id}/anonymize")
async def anonymize_user(
    user_id: str,
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Anonymize user data (KVKK right to be forgotten).
    Replaces PII with anonymized values.
    """
    try:
        # Get user
        result = await db.execute(
            select(Customer).where(Customer.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Store original data for audit
        original_data = {
            "customer_id": user.customer_id,
            "email": user.email,
            "phone": user.phone
        }
        
        # Anonymize
        user.first_name = "ANONYMIZED"
        user.last_name = "ANONYMIZED"
        user.email = f"anonymized_{user.id}@deleted.local"
        user.phone = "ANONYMIZED"
        user.status = CustomerStatus.INACTIVE
        
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.ANONYMIZE,
            resource_type="customer",
            admin_user_id=str(current_admin.id),
            resource_id=str(user.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={
                "action": "User anonymized (KVKK)",
                "original_customer_id": original_data["customer_id"]
            }
        )
        db.add(audit_log)
        
        await db.commit()
        
        logger.info("user_anonymized", admin_id=str(current_admin.id), user_id=user_id)
        
        return {"message": "User anonymized successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("anonymize_user_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to anonymize user"
        )
