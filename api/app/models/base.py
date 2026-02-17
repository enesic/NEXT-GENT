from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import MetaData, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

# Naming convention for constraints to avoid alembic issues
POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

class TenantMixin:
    """
    Mixin to add tenant context to a model.
    """
    @declared_attr
    def tenant_id(cls) -> Mapped[UUID]:
        # Using UUID for tenant_id. Index for faster lookups.
        return mapped_column(index=True, nullable=False)
