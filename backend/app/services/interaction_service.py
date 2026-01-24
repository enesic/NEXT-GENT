from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.interaction import Interaction, InteractionStatus
from app.models.tenant import Tenant
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    InteractionConflict
)
from app.services.webhook_service import WebhookService


class InteractionService:
    """
    Service layer for interaction management with concurrency control.
    Handles Appointments, Court Hearings, Property Viewings, etc.
    """

    @staticmethod
    async def check_time_slot_availability(
        db: AsyncSession,
        tenant_id: UUID,
        start_time: datetime,
        end_time: datetime,
        exclude_interaction_id: Optional[UUID] = None
    ) -> bool:
        """
        Check if a time slot is available (no conflicts).
        """
        query = select(Interaction).where(
            and_(
                Interaction.tenant_id == tenant_id,
                Interaction.status.in_([InteractionStatus.PENDING, InteractionStatus.CONFIRMED]),
                or_(
                    # New interaction starts during existing interaction
                    and_(
                        Interaction.start_time <= start_time,
                        Interaction.end_time > start_time
                    ),
                    # New interaction ends during existing interaction
                    and_(
                        Interaction.start_time < end_time,
                        Interaction.end_time >= end_time
                    ),
                    # New interaction completely contains existing interaction
                    and_(
                        Interaction.start_time >= start_time,
                        Interaction.end_time <= end_time
                    )
                )
            )
        )
        
        if exclude_interaction_id:
            query = query.where(Interaction.id != exclude_interaction_id)
        
        result = await db.execute(query)
        conflicts = result.scalars().all()
        
        return len(conflicts) == 0

    @staticmethod
    async def get_conflicting_interactions(
        db: AsyncSession,
        tenant_id: UUID,
        start_time: datetime,
        end_time: datetime,
        exclude_interaction_id: Optional[UUID] = None
    ) -> List[InteractionConflict]:
        """
        Get list of conflicting interaction for a given time slot.
        """
        query = select(Interaction).where(
            and_(
                Interaction.tenant_id == tenant_id,
                Interaction.status.in_([InteractionStatus.PENDING, InteractionStatus.CONFIRMED]),
                or_(
                    and_(
                        Interaction.start_time <= start_time,
                        Interaction.end_time > start_time
                    ),
                    and_(
                        Interaction.start_time < end_time,
                        Interaction.end_time >= end_time
                    ),
                    and_(
                        Interaction.start_time >= start_time,
                        Interaction.end_time <= end_time
                    )
                )
            )
        )
        
        if exclude_interaction_id:
            query = query.where(Interaction.id != exclude_interaction_id)
        
        result = await db.execute(query)
        conflicts = result.scalars().all()
        
        return [
            InteractionConflict(
                conflicting_interaction_id=intr.id,
                start_time=intr.start_time,
                end_time=intr.end_time,
                title=intr.title
            )
            for intr in conflicts
        ]

    @staticmethod
    async def create_interaction(
        db: AsyncSession,
        tenant_id: UUID,
        interaction_data: InteractionCreate
    ) -> Interaction:
        """
        Create a new interaction with conflict checking.
        """
        # Step 1: Check if time slot is available
        is_available = await InteractionService.check_time_slot_availability(
            db=db,
            tenant_id=tenant_id,
            start_time=interaction_data.start_time,
            end_time=interaction_data.end_time
        )
        
        if not is_available:
            conflicts = await InteractionService.get_conflicting_interactions(
                db=db,
                tenant_id=tenant_id,
                start_time=interaction_data.start_time,
                end_time=interaction_data.end_time
            )
            
            # Notify about conflict via webhook
            tenant_query = select(Tenant).where(Tenant.id == tenant_id)
            tenant_result = await db.execute(tenant_query)
            tenant = tenant_result.scalar_one_or_none()
            
            if tenant and tenant.webhook_url:
                # Assuming generic webhook notification for conflict
                await WebhookService.notify_appointment_conflict(
                    appointment_data=interaction_data.model_dump(mode='json'),
                    conflicts=[conflict.model_dump() for conflict in conflicts],
                    webhook_url=tenant.webhook_url
                )
            
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Time slot is not available",
                    "conflicts": [conflict.model_dump() for conflict in conflicts]
                }
        )
        
        # Step 2: Create interaction
        interaction = Interaction(
            **interaction_data.model_dump(),
            tenant_id=tenant_id,
            status=InteractionStatus.PENDING
        )
        
        db.add(interaction)
        
        try:
            await db.commit()
            await db.refresh(interaction)
        except IntegrityError as e:
            await db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            
            if 'idx_interactions_no_overlap' in error_msg or 'duplicate key' in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message": "Bu saat dilimi az önce doldu. Lütfen başka bir saat seçin.",
                        "error_code": "TIME_SLOT_JUST_TAKEN"
                    }
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create interaction"
                )
        
        # Step 3: Webhook notification
        tenant_query = select(Tenant).where(Tenant.id == tenant_id)
        tenant_result = await db.execute(tenant_query)
        tenant = tenant_result.scalar_one_or_none()
        
        if tenant and tenant.webhook_url:
            # We might need to update WebhookService to handle "interaction" or alias it
            await WebhookService.notify_appointment_created(
                db=db,
                appointment=interaction, # Passing interaction as appointment for now
                webhook_url=tenant.webhook_url
            )
        
        return interaction

    @staticmethod
    async def update_interaction(
        db: AsyncSession,
        tenant_id: UUID,
        interaction_id: UUID,
        interaction_data: InteractionUpdate,
        current_version: int
    ) -> Interaction:
        """
        Update an interaction with optimistic locking.
        """
        query = select(Interaction).where(
            and_(
                Interaction.id == interaction_id,
                Interaction.tenant_id == tenant_id,
                Interaction.version == current_version
            )
        )
        
        result = await db.execute(query)
        interaction = result.scalar_one_or_none()
        
        if not interaction:
            # Version mismatch check
            check_query = select(Interaction).where(
                and_(
                    Interaction.id == interaction_id,
                    Interaction.tenant_id == tenant_id
                )
            )
            check_result = await db.execute(check_query)
            exists = check_result.scalar_one_or_none()
            
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Interaction was modified by another user. Please refresh and try again."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Interaction not found"
                )
        
        update_dict = interaction_data.model_dump(exclude_unset=True)
        
        if 'start_time' in update_dict or 'end_time' in update_dict:
            new_start = update_dict.get('start_time', interaction.start_time)
            new_end = update_dict.get('end_time', interaction.end_time)
            
            is_available = await InteractionService.check_time_slot_availability(
                db=db,
                tenant_id=tenant_id,
                start_time=new_start,
                end_time=new_end,
                exclude_interaction_id=interaction_id
            )
            
            if not is_available:
                conflicts = await InteractionService.get_conflicting_interactions(
                    db=db,
                    tenant_id=tenant_id,
                    start_time=new_start,
                    end_time=new_end,
                    exclude_interaction_id=interaction_id
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message": "New time slot is not available",
                        "conflicts": [conflict.model_dump() for conflict in conflicts]
                    }
                )
        
        for field, value in update_dict.items():
            setattr(interaction, field, value)
        
        interaction.version += 1
        
        try:
            await db.commit()
            await db.refresh(interaction)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update interaction"
            )
        
        # Webhook notification
        tenant_query = select(Tenant).where(Tenant.id == tenant_id)
        tenant_result = await db.execute(tenant_query)
        tenant = tenant_result.scalar_one_or_none()
        
        if tenant and tenant.webhook_url:
            await WebhookService.notify_appointment_updated(
                appointment=interaction,
                webhook_url=tenant.webhook_url,
                changes=update_dict
            )
        
        return interaction

    @staticmethod
    async def get_interaction(
        db: AsyncSession,
        tenant_id: UUID,
        interaction_id: UUID
    ) -> Optional[Interaction]:
        """Get a single interaction by ID."""
        query = select(Interaction).where(
            and_(
                Interaction.id == interaction_id,
                Interaction.tenant_id == tenant_id
            )
        )
        
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_interactions(
        db: AsyncSession,
        tenant_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[InteractionStatus] = None,
        type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interaction]:
        """
        List interactions with optional filters.
        """
        query = select(Interaction).where(Interaction.tenant_id == tenant_id)
        
        if start_date:
            query = query.where(Interaction.start_time >= start_date)
        
        if end_date:
            query = query.where(Interaction.end_time <= end_date)
        
        if status:
            query = query.where(Interaction.status == status)
            
        if type:
            query = query.where(Interaction.type == type)
        
        query = query.order_by(Interaction.start_time).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def cancel_interaction(
        db: AsyncSession,
        tenant_id: UUID,
        interaction_id: UUID
    ) -> Interaction:
        """Cancel an interaction."""
        interaction = await InteractionService.get_interaction(db, tenant_id, interaction_id)
        
        if not interaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interaction not found"
            )
        
        if interaction.status == InteractionStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interaction is already cancelled"
            )
        
        interaction.status = InteractionStatus.CANCELLED
        interaction.version += 1
        
        await db.commit()
        await db.refresh(interaction)
        
        # Webhook notification
        tenant_query = select(Tenant).where(Tenant.id == tenant_id)
        tenant_result = await db.execute(tenant_query)
        tenant = tenant_result.scalar_one_or_none()
        
        if tenant and tenant.webhook_url:
            await WebhookService.notify_appointment_cancelled(
                appointment=interaction,
                webhook_url=tenant.webhook_url
            )
        
        return interaction
