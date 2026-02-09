from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.validation import ContextValidator
from app.core.security.masking import KVKKMasker
from app.models.tenant import Tenant
from app.models.interaction import InteractionStatus
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    InteractionConflict
)
# Assuming service renaming happens next, referencing existing for now or renaming import
# For this step, I will rename the service file as well to keep consistency
from app.services.interaction_service import InteractionService

router = APIRouter()


@router.post("/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    interaction_in: InteractionCreate,
):
    """
    Create a new interaction (appointment, case, etc.).
    
    Validates metadata against tenant configuration rules.
    Checks for time slot conflicts.
    """
    # 1. Dynamic Metadata Validation
    if interaction_in.metadata:
        try:
            # Get validation rules from tenant config or default sector rules
            sector = current_tenant.config.get('sector') if current_tenant.config else "medical"
            rules = current_tenant.config.get('validation_rules') if current_tenant.config else ContextValidator.get_sector_rules(sector)
            
            validated_metadata = ContextValidator.validate_metadata(interaction_in.metadata, rules)
            interaction_in.metadata = validated_metadata # Keep as metadata for Pydantic model
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )

    # 2. Create Interaction via Service
    interaction = await InteractionService.create_interaction(
        db=db,
        tenant_id=current_tenant.id,
        interaction_data=interaction_in
    )
    return interaction


@router.get("/", response_model=List[InteractionResponse])
async def list_interactions(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    status: Optional[InteractionStatus] = Query(None, description="Filter by status"),
    type: Optional[str] = Query(None, description="Filter by interaction type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List interactions with optional filters.
    Applies KVKK masking to sensitive metadata fields.
    """
    interactions = await InteractionService.list_interactions(
        db=db,
        tenant_id=current_tenant.id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        type=type,
        skip=skip,
        limit=limit
    )
    
    # Apply KVKK Masking
    sector = current_tenant.config.get('sector') if current_tenant.config else "medical"
    privacy_rules = current_tenant.config.get('privacy_rules') if current_tenant.config else KVKKMasker.get_privacy_rules(sector)
    
    for interaction in interactions:
        if interaction.meta_data:
            interaction.meta_data = KVKKMasker.mask_data(interaction.meta_data, privacy_rules)
            
    return interactions


@router.get("/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    interaction_id: UUID,
):
    """
    Get a specific interaction by ID.
    """
    interaction = await InteractionService.get_interaction(
        db=db,
        tenant_id=current_tenant.id,
        interaction_id=interaction_id
    )
    
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    
    # Apply KVKK Masking
    sector = current_tenant.config.get('sector') if current_tenant.config else "medical"
    privacy_rules = current_tenant.config.get('privacy_rules') if current_tenant.config else KVKKMasker.get_privacy_rules(sector)
    
    if interaction.meta_data:
        interaction.meta_data = KVKKMasker.mask_data(interaction.meta_data, privacy_rules)
    
    return interaction


@router.put("/{interaction_id}", response_model=InteractionResponse)
async def update_interaction(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    interaction_id: UUID,
    interaction_in: InteractionUpdate,
    version: int = Query(..., description="Current version for optimistic locking"),
):
    """
    Update an interaction.
    """
    # Validate metadata if present
    if interaction_in.metadata:
        try:
             # Get validation rules
            sector = current_tenant.config.get('sector') if current_tenant.config else "medical"
            rules = current_tenant.config.get('validation_rules') if current_tenant.config else ContextValidator.get_sector_rules(sector)
            
            validated_metadata = ContextValidator.validate_metadata(interaction_in.metadata, rules)
            interaction_in.meta_data = validated_metadata
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )

    interaction = await InteractionService.update_interaction(
        db=db,
        tenant_id=current_tenant.id,
        interaction_id=interaction_id,
        interaction_data=interaction_in,
        current_version=version
    )
    return interaction


@router.post("/{interaction_id}/cancel", response_model=InteractionResponse)
async def cancel_interaction(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    interaction_id: UUID,
):
    """
    Cancel an interaction.
    """
    interaction = await InteractionService.cancel_interaction(
        db=db,
        tenant_id=current_tenant.id,
        interaction_id=interaction_id
    )
    return interaction


@router.get("/check-availability/", response_model=dict)
async def check_availability(
    *,
    db: AsyncSession = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
    start_time: datetime = Query(..., description="Start time to check"),
    end_time: datetime = Query(..., description="End time to check"),
):
    """
    Check if a time slot is available.
    """
    is_available = await InteractionService.check_time_slot_availability(
        db=db,
        tenant_id=current_tenant.id,
        start_time=start_time,
        end_time=end_time
    )
    
    conflicts = []
    if not is_available:
        conflicts = await InteractionService.get_conflicting_interactions(
            db=db,
            tenant_id=current_tenant.id,
            start_time=start_time,
            end_time=end_time
        )
    
    return {
        "available": is_available,
        "conflicts": [conflict.model_dump() for conflict in conflicts]
    }
