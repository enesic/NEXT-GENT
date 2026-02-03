from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Text, Integer, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin
from app.core.encrypted_types import EncryptedString
from app.core.encryption import encryption_service


class CustomerSegment(str, enum.Enum):
    """Müşteri segment tipleri"""
    VIP = "vip"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    REGULAR = "regular"


class CustomerStatus(str, enum.Enum):
    """Müşteri durumu"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    DEBT = "debt"  # Borçlu müşteri


class Customer(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "customers"

    # Temel Bilgiler (PII - Encrypted)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    # Phone - ENCRYPTED for PII protection
    phone: Mapped[str] = mapped_column(EncryptedString(50), nullable=False)
    # Phone hash for searchable lookup (cannot be reversed to get actual phone)
    phone_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True, unique=True)
    
    # ID-Based Authentication (NEW)
    customer_id: Mapped[str] = mapped_column(String(20), nullable=True, unique=True, index=True)
    # Format: SECTOR-NNNNNN (e.g., MED-001234, LEG-005678)
    
    pin_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    # Bcrypt hashed PIN for authentication
    
    # Adres Bilgileri
    address: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # CRM Bilgileri
    segment: Mapped[CustomerSegment] = mapped_column(
        SQLEnum(CustomerSegment, name="customer_segment"),
        default=CustomerSegment.REGULAR,
        nullable=False,
        index=True
    )
    status: Mapped[CustomerStatus] = mapped_column(
        SQLEnum(CustomerStatus, name="customer_status"),
        default=CustomerStatus.ACTIVE,
        nullable=False,
        index=True
    )
    
    # İstatistikler
    total_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_spent: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    lifetime_value: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    
    # Borç Bilgisi
    debt_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    
    # Son Aktivite
    last_order_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_contact_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Notlar
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Referans
    referral_code: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    referred_by: Mapped[str] = mapped_column(String(50), nullable=True)  # Referral code of referrer

    def set_phone(self, phone: str):
        """
        Set phone number with automatic hash generation for lookup.
        Use this method instead of directly setting phone attribute.
        """
        self.phone = phone
        self.phone_hash = encryption_service.hash_phone_for_lookup(phone)
    
    @staticmethod
    def generate_phone_hash(phone: str) -> str:
        """Generate hash for phone lookup without setting the phone."""
        return encryption_service.hash_phone_for_lookup(phone)
