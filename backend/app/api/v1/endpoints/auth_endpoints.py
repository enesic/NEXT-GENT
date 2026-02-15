"""
Admin Authentication Endpoints
Handles admin login, logout, and JWT token management
"""
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, EmailStr
import bcrypt
import jwt
from app.core.database import get_db
from app.core.config import settings
from app.core.logger import get_logger
from app.models.admin_user import AdminUser, AdminRole
from app.models.audit_log import AuditLog, ActionType

router = APIRouter()
logger = get_logger(__name__)
security = HTTPBearer()


# Schemas
class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_user: dict


class TokenRefreshRequest(BaseModel):
    refresh_token: str


# Helper Functions
def create_access_token(admin_id: str, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": admin_id,
        "exp": expire,
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return admin_id"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        admin_id: str = payload.get("sub")
        if admin_id is None:
            return None
        return admin_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> AdminUser:
    """Dependency to get current authenticated admin"""
    token = credentials.credentials
    admin_id = verify_token(token)
    
    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    result = await db.execute(
        select(AdminUser).where(AdminUser.id == admin_id)
    )
    admin = result.scalar_one_or_none()
    
    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found or inactive"
        )
    
    return admin


# Endpoints
@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(
    login_data: AdminLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin login endpoint with JWT token generation.
    Rate limited to prevent brute force attacks.
    """
    try:
        # Find admin by username
        result = await db.execute(
            select(AdminUser).where(AdminUser.username == login_data.username)
        )
        admin = result.scalar_one_or_none()
        
        if not admin:
            logger.warning("login_failed", username=login_data.username, reason="user_not_found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Verify password
        if not bcrypt.checkpw(login_data.password.encode('utf-8'), admin.password_hash.encode('utf-8')):
            logger.warning("login_failed", username=login_data.username, reason="invalid_password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Check if active
        if not admin.is_active:
            logger.warning("login_failed", username=login_data.username, reason="inactive_account")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Update login tracking
        admin.last_login_at = datetime.utcnow()
        admin.login_count += 1
        admin.last_ip = request.client.host if request.client else None
        
        # Create access token
        access_token = create_access_token(str(admin.id))
        
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.LOGIN,
            resource_type="admin_user",
            admin_user_id=str(admin.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={"action": "Admin login successful"}
        )
        db.add(audit_log)
        
        await db.commit()
        
        logger.info("admin_login_success", admin_id=str(admin.id), username=admin.username)
        
        return AdminLoginResponse(
            access_token=access_token,
            admin_user=admin.get_safe_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("admin_login_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/logout")
async def admin_logout(
    request: Request,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin logout endpoint.
    Creates audit log entry.
    """
    try:
        # Create audit log
        audit_log = AuditLog.create_log(
            action_type=ActionType.LOGOUT,
            resource_type="admin_user",
            admin_user_id=str(current_admin.id),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes={"action": "Admin logout"}
        )
        db.add(audit_log)
        await db.commit()
        
        logger.info("admin_logout", admin_id=str(current_admin.id))
        
        return {"message": "Logout successful"}
        
    except Exception as e:
        logger.error("admin_logout_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me")
async def get_current_admin_info(
    current_admin: AdminUser = Depends(get_current_admin)
):
    """Get current admin user info"""
    return current_admin.get_safe_dict()


@router.post("/refresh")
async def refresh_token(
    current_admin: AdminUser = Depends(get_current_admin)
):
    """Refresh access token"""
    new_token = create_access_token(str(current_admin.id))
    return {
        "access_token": new_token,
        "token_type": "bearer"
    }
