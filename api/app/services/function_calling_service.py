"""
Function Calling Service - Allows AI to automatically execute system functions.
"""
from typing import Dict, Any, Optional, Callable
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.services.interaction_service import InteractionService
from app.services.customer_service import CustomerService
from app.schemas.interaction import InteractionCreate

logger = get_logger(__name__)


class FunctionCallingService:
    """
    Service for executing functions that AI can call automatically.
    """
    
    # Function registry
    _functions: Dict[str, Callable] = {}
    
    @classmethod
    def register_function(cls, name: str, func: Callable):
        """Register a function that AI can call."""
        cls._functions[name] = func
        logger.info("function_registered", function_name=name)
    
    @classmethod
    async def execute_function(
        cls,
        function_name: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a function by name.
        
        Args:
            function_name: Name of function to execute
            parameters: Function parameters
            context: Additional context (tenant_id, db session, etc.)
            
        Returns:
            Execution result
        """
        if function_name not in cls._functions:
            logger.error("function_not_found", function_name=function_name)
            return {
                "success": False,
                "error": f"Function '{function_name}' not found"
            }
        
        try:
            func = cls._functions[function_name]
            result = await func(parameters, context)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error("function_execution_error", function=function_name, error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    @classmethod
    def get_available_functions(cls) -> List[Dict[str, Any]]:
        """Get list of available functions for AI."""
        return [
            {
                "name": "create_appointment",
                "description": "Create a new appointment/interaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Appointment title"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                        "time": {"type": "string", "description": "Time in HH:MM format"},
                        "customer_name": {"type": "string"},
                        "customer_phone": {"type": "string"},
                        "customer_email": {"type": "string"},
                        "type": {"type": "string", "description": "Interaction type (appointment, consultation, etc.)"}
                    },
                    "required": ["title", "date", "time", "customer_name"]
                }
            },
            {
                "name": "cancel_appointment",
                "description": "Cancel an existing appointment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "string", "description": "Appointment ID"},
                        "reason": {"type": "string", "description": "Cancellation reason"}
                    },
                    "required": ["appointment_id"]
                }
            },
            {
                "name": "get_customer_info",
                "description": "Get customer information by phone or email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phone": {"type": "string"},
                        "email": {"type": "string"}
                    }
                }
            },
            {
                "name": "send_satisfaction_survey",
                "description": "Send satisfaction survey to customer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"},
                        "interaction_id": {"type": "string"}
                    },
                    "required": ["customer_id"]
                }
            }
        ]


# Register functions
async def _create_appointment(params: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Create appointment function."""
    if not context:
        raise ValueError("Context is required (db, tenant_id)")
    
    db: AsyncSession = context.get("db")
    tenant_id: UUID = context.get("tenant_id")
    
    if not db or not tenant_id:
        raise ValueError("db and tenant_id are required in context")
    
    # Parse date and time
    date_str = params.get("date")
    time_str = params.get("time")
    
    if not date_str or not time_str:
        raise ValueError("Date and time are required")
    
    # Combine date and time
    datetime_str = f"{date_str} {time_str}"
    start_time = datetime.fromisoformat(datetime_str.replace(" ", "T"))
    end_time = start_time.replace(hour=start_time.hour + 1)  # Default 1 hour duration
    
    # Create interaction
    interaction_data = InteractionCreate(
        title=params.get("title", "AI Created Appointment"),
        description=f"Created automatically by AI assistant",
        type=params.get("type", "appointment"),
        start_time=start_time,
        end_time=end_time,
        client_name=params.get("customer_name", "Unknown"),
        client_email=params.get("customer_email", ""),
        client_phone=params.get("customer_phone", "")
    )
    
    interaction = await InteractionService.create_interaction(
        db=db,
        tenant_id=tenant_id,
        interaction_data=interaction_data
    )
    
    return {
        "appointment_id": str(interaction.id),
        "message": f"Randevunuz {date_str} tarihinde {time_str} saatinde oluşturuldu."
    }


async def _cancel_appointment(params: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Cancel appointment function."""
    if not context:
        raise ValueError("Context is required")
    
    db: AsyncSession = context.get("db")
    tenant_id: UUID = context.get("tenant_id")
    
    if not db or not tenant_id:
        raise ValueError("db and tenant_id are required in context")
    
    appointment_id = UUID(params.get("appointment_id"))
    
    interaction = await InteractionService.cancel_interaction(
        db=db,
        tenant_id=tenant_id,
        interaction_id=appointment_id
    )
    
    return {
        "message": "Randevunuz iptal edildi.",
        "appointment_id": str(interaction.id)
    }


async def _get_customer_info(params: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Get customer info function."""
    if not context:
        raise ValueError("Context is required")
    
    db: AsyncSession = context.get("db")
    tenant_id: UUID = context.get("tenant_id")
    
    if not db or not tenant_id:
        raise ValueError("db and tenant_id are required in context")
    
    phone = params.get("phone")
    email = params.get("email")
    
    if phone:
        customer, _ = await CustomerService.get_customer_by_phone(
            db=db,
            tenant_id=tenant_id,
            phone=phone
        )
    elif email:
        # Query by email
        from sqlalchemy import select
        from app.models.customer import Customer
        query = select(Customer).where(
            Customer.tenant_id == tenant_id,
            Customer.email == email
        )
        result = await db.execute(query)
        customer = result.scalar_one_or_none()
    else:
        raise ValueError("Phone or email is required")
    
    if not customer:
        return {
            "found": False,
            "message": "Müşteri bulunamadı."
        }
    
    return {
        "found": True,
        "customer": {
            "name": f"{customer.first_name} {customer.last_name}",
            "email": customer.email,
            "phone": customer.phone,
            "segment": customer.segment.value,
            "status": customer.status.value
        }
    }



async def _send_satisfaction_survey(params: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Send satisfaction survey function."""
    if not context:
        raise ValueError("Context is required")
    
    db: AsyncSession = context.get("db")
    tenant_id: UUID = context.get("tenant_id")
    
    if not db or not tenant_id:
        raise ValueError("db and tenant_id are required in context")
    
    customer_id = params.get("customer_id")
    interaction_id = params.get("interaction_id")
    
    # Get customer info
    from sqlalchemy import select
    from app.models.customer import Customer
    from app.models.satisfaction import Satisfaction, SatisfactionType, SatisfactionChannel
    
    query = select(Customer).where(
        Customer.tenant_id == tenant_id,
        Customer.id == UUID(customer_id)
    )
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise ValueError("Customer not found")
    
    # Create satisfaction record (pending response)
    satisfaction = Satisfaction(
        tenant_id=tenant_id,
        customer_id=customer_id,
        interaction_id=interaction_id,
        survey_type=SatisfactionType.CSAT,
        channel=SatisfactionChannel.SMS,  # Default to SMS
        survey_sent_at=datetime.utcnow()
    )
    
    db.add(satisfaction)
    await db.commit()
    await db.refresh(satisfaction)
    
    # Generate survey link
    survey_link = f"https://survey.nextgent.com/{satisfaction.id}"
    
    # TODO: Integrate with SMS/Email service to actually send the survey
    # For now, we just log it
    logger.info(
        "survey_sent",
        customer_id=customer_id,
        survey_id=str(satisfaction.id),
        phone=customer.phone,
        link=survey_link
    )
    
    return {
        "message": f"Memnuniyet anketi {customer.first_name} {customer.last_name} adlı müşteriye gönderildi.",
        "customer_id": customer_id,
        "survey_id": str(satisfaction.id),
        "survey_link": survey_link
    }


# Register all functions
FunctionCallingService.register_function("create_appointment", _create_appointment)
FunctionCallingService.register_function("cancel_appointment", _cancel_appointment)
FunctionCallingService.register_function("get_customer_info", _get_customer_info)
FunctionCallingService.register_function("send_satisfaction_survey", _send_satisfaction_survey)
