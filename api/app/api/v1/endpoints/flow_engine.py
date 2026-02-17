"""
Automation Flow Engine API endpoints.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from pydantic import BaseModel
import uuid as uuid_pkg

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.logger import get_logger
from app.models.tenant import Tenant
from app.models.flow import Flow, FlowExecution

router = APIRouter()
logger = get_logger(__name__)


# Schemas
class FlowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    config: Dict[str, Any]
    is_active: bool = True
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    priority: int = 0


class FlowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = None


class FlowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    config: Dict[str, Any]
    is_active: bool
    is_template: bool
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    category: Optional[str]
    tags: List[str]
    priority: int
    created_at: datetime
    updated_at: datetime


class FlowExecutionResponse(BaseModel):
    id: str
    flow_id: str
    status: str
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    execution_time_ms: Optional[int]
    executed_actions: List[str]
    created_at: datetime


@router.get("/", response_model=List[FlowResponse])
async def list_flows(
    is_active: Optional[bool] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    List all automation flows.
    """
    try:
        query = select(Flow)
        
        conditions = []
        if current_tenant:
            conditions.append(Flow.tenant_id == current_tenant.id)
        if is_active is not None:
            conditions.append(Flow.is_active == is_active)
        if category:
            conditions.append(Flow.category == category)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(desc(Flow.priority), desc(Flow.created_at))
        
        result = await db.execute(query)
        flows = result.scalars().all()
        
        return [
            FlowResponse(
                id=str(flow.id),
                name=flow.name,
                description=flow.description,
                config=flow.config,
                is_active=flow.is_active,
                is_template=flow.is_template,
                total_executions=flow.total_executions,
                successful_executions=flow.successful_executions,
                failed_executions=flow.failed_executions,
                success_rate=(flow.successful_executions / flow.total_executions * 100) if flow.total_executions > 0 else 0,
                category=flow.category,
                tags=flow.tags or [],
                priority=flow.priority,
                created_at=flow.created_at,
                updated_at=flow.updated_at
            )
            for flow in flows
        ]
        
    except Exception as e:
        logger.error("list_flows_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow listesi alınamadı"
        )


@router.post("/", response_model=FlowResponse)
async def create_flow(
    flow_data: FlowCreate,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Create a new automation flow.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant bilgisi gerekli"
            )
        
        new_flow = Flow(
            tenant_id=current_tenant.id,
            name=flow_data.name,
            description=flow_data.description,
            config=flow_data.config,
            is_active=flow_data.is_active,
            category=flow_data.category,
            tags=flow_data.tags,
            priority=flow_data.priority
        )
        
        db.add(new_flow)
        await db.commit()
        await db.refresh(new_flow)
        
        logger.info("flow_created", flow_id=str(new_flow.id), name=new_flow.name)
        
        return FlowResponse(
            id=str(new_flow.id),
            name=new_flow.name,
            description=new_flow.description,
            config=new_flow.config,
            is_active=new_flow.is_active,
            is_template=new_flow.is_template,
            total_executions=0,
            successful_executions=0,
            failed_executions=0,
            success_rate=0,
            category=new_flow.category,
            tags=new_flow.tags or [],
            priority=new_flow.priority,
            created_at=new_flow.created_at,
            updated_at=new_flow.updated_at
        )
        
    except Exception as e:
        logger.error("create_flow_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow oluşturulamadı"
        )


@router.put("/{flow_id}", response_model=FlowResponse)
async def update_flow(
    flow_id: str,
    flow_data: FlowUpdate,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Update an existing flow.
    """
    try:
        result = await db.execute(
            select(Flow).where(Flow.id == uuid_pkg.UUID(flow_id))
        )
        flow = result.scalar_one_or_none()
        
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow bulunamadı"
            )
        
        # Update fields
        if flow_data.name is not None:
            flow.name = flow_data.name
        if flow_data.description is not None:
            flow.description = flow_data.description
        if flow_data.config is not None:
            flow.config = flow_data.config
        if flow_data.is_active is not None:
            flow.is_active = flow_data.is_active
        if flow_data.category is not None:
            flow.category = flow_data.category
        if flow_data.tags is not None:
            flow.tags = flow_data.tags
        if flow_data.priority is not None:
            flow.priority = flow_data.priority
        
        await db.commit()
        await db.refresh(flow)
        
        logger.info("flow_updated", flow_id=str(flow.id))
        
        return FlowResponse(
            id=str(flow.id),
            name=flow.name,
            description=flow.description,
            config=flow.config,
            is_active=flow.is_active,
            is_template=flow.is_template,
            total_executions=flow.total_executions,
            successful_executions=flow.successful_executions,
            failed_executions=flow.failed_executions,
            success_rate=(flow.successful_executions / flow.total_executions * 100) if flow.total_executions > 0 else 0,
            category=flow.category,
            tags=flow.tags or [],
            priority=flow.priority,
            created_at=flow.created_at,
            updated_at=flow.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("update_flow_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow güncellenemedi"
        )


@router.delete("/{flow_id}")
async def delete_flow(
    flow_id: str,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Delete a flow.
    """
    try:
        result = await db.execute(
            select(Flow).where(Flow.id == uuid_pkg.UUID(flow_id))
        )
        flow = result.scalar_one_or_none()
        
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow bulunamadı"
            )
        
        await db.delete(flow)
        await db.commit()
        
        logger.info("flow_deleted", flow_id=flow_id)
        
        return {"message": "Flow başarıyla silindi", "flow_id": flow_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("delete_flow_error", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow silinemedi"
        )


@router.post("/{flow_id}/execute")
async def execute_flow(
    flow_id: str,
    input_data: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Execute a flow manually.
    """
    try:
        result = await db.execute(
            select(Flow).where(Flow.id == uuid_pkg.UUID(flow_id))
        )
        flow = result.scalar_one_or_none()
        
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow bulunamadı"
            )
        
        if not flow.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Flow aktif değil"
            )
        
        # Execute flow in background
        if background_tasks:
            background_tasks.add_task(
                execute_flow_task,
                flow_id=flow.id,
                tenant_id=current_tenant.id if current_tenant else None,
                input_data=input_data or {},
                db=db
            )
        
        return {
            "message": "Flow çalıştırılıyor",
            "flow_id": flow_id,
            "status": "queued"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("execute_flow_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow çalıştırılamadı"
        )


async def execute_flow_task(flow_id: uuid_pkg.UUID, tenant_id: Optional[uuid_pkg.UUID], input_data: Dict[str, Any], db: AsyncSession):
    """
    Background task to execute flow.
    """
    start_time = datetime.utcnow()
    
    try:
        # Placeholder for actual flow execution logic
        # This would involve:
        # 1. Evaluating trigger conditions
        # 2. Running actions (send SMS, email, webhook, etc.)
        # 3. Handling fallback actions on failure
        
        execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        # Create execution record
        execution = FlowExecution(
            flow_id=flow_id,
            tenant_id=tenant_id,
            status="success",
            input_data=input_data,
            output_data={"result": "Flow executed successfully"},
            execution_time_ms=execution_time_ms,
            executed_actions=["action_1", "action_2"]
        )
        
        db.add(execution)
        
        # Update flow stats
        result = await db.execute(
            select(Flow).where(Flow.id == flow_id)
        )
        flow = result.scalar_one_or_none()
        if flow:
            flow.total_executions += 1
            flow.successful_executions += 1
        
        await db.commit()
        
        logger.info("flow_executed", flow_id=str(flow_id), execution_time_ms=execution_time_ms)
        
    except Exception as e:
        logger.error("flow_execution_failed", flow_id=str(flow_id), error=str(e))
        
        # Create failed execution record
        execution = FlowExecution(
            flow_id=flow_id,
            tenant_id=tenant_id,
            status="failed",
            input_data=input_data,
            error_message=str(e),
            execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
        )
        
        db.add(execution)
        
        # Update flow stats
        result = await db.execute(
            select(Flow).where(Flow.id == flow_id)
        )
        flow = result.scalar_one_or_none()
        if flow:
            flow.total_executions += 1
            flow.failed_executions += 1
        
        await db.commit()


@router.get("/{flow_id}/executions", response_model=List[FlowExecutionResponse])
async def get_flow_executions(
    flow_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get execution history for a flow.
    """
    try:
        result = await db.execute(
            select(FlowExecution)
            .where(FlowExecution.flow_id == uuid_pkg.UUID(flow_id))
            .order_by(desc(FlowExecution.created_at))
            .limit(limit)
        )
        executions = result.scalars().all()
        
        return [
            FlowExecutionResponse(
                id=str(execution.id),
                flow_id=str(execution.flow_id),
                status=execution.status,
                input_data=execution.input_data,
                output_data=execution.output_data,
                error_message=execution.error_message,
                execution_time_ms=execution.execution_time_ms,
                executed_actions=execution.executed_actions or [],
                created_at=execution.created_at
            )
            for execution in executions
        ]
        
    except Exception as e:
        logger.error("get_executions_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Execution geçmişi alınamadı"
        )
