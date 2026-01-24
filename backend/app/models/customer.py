from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Text, Integer, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin, TenantMixin


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

    # Temel Bilgiler
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    
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
