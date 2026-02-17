"""
Admin User Model - For system administrators with enhanced permissions
"""
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models.base import Base, UUIDMixin, TimestampMixin


class AdminRole(str):
    """Admin role constants"""
    SUPER_ADMIN = "super_admin"  # Full system access
    ADMIN = "admin"  # Standard admin access
    MODERATOR = "moderator"  # Limited admin access


class AdminUser(Base, UUIDMixin, TimestampMixin):
    """
    Admin user model with role-based permissions.
    Used for system administration, monitoring, and KVKK compliance tasks.
    """
    __tablename__ = "admin_users"

    # Basic Info
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    # Role and Status
    role: Mapped[str] = mapped_column(String, default=AdminRole.ADMIN, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Permissions (JSONB for granular control)
    # Example: {
    #   "users": ["create", "read", "update", "delete"],
    #   "logs": ["read", "export"],
    #   "analytics": ["read"],
    #   "settings": ["update"]
    # }
    permissions: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    # Activity Tracking
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    login_count: Mapped[int] = mapped_column(default=0, nullable=False)
    last_ip: Mapped[str] = mapped_column(String, nullable=True)
    
    # 2FA (Optional)
    two_factor_secret: Mapped[str] = mapped_column(String, nullable=True)
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<AdminUser {self.username} ({self.role})>"
    
    def has_permission(self, resource: str, action: str) -> bool:
        """
        Check if admin has specific permission.
        Super admins have all permissions.
        """
        if self.is_super_admin:
            return True
        
        if not self.permissions:
            return False
            
        resource_perms = self.permissions.get(resource, [])
        return action in resource_perms
    
    def get_safe_dict(self) -> dict:
        """Return safe dictionary without sensitive data"""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "is_super_admin": self.is_super_admin,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "login_count": self.login_count,
            "two_factor_enabled": self.two_factor_enabled
        }
