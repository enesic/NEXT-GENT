import httpx
import structlog
import time
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.interaction import Interaction, InteractionStatus
from app.models.failed_webhook import FailedWebhook, WebhookStatus

# Configure structured logging
logger = structlog.get_logger(__name__)


class WebhookService:
    """
    Enterprise-grade webhook service with retry mechanism and failure tracking.
    
    Features:
    - Exponential backoff retry (1s, 2s, 4s)
    - 5-second timeout
    - Structured logging with latency tracking
    - Failed webhook persistence for manual retry
    """
    
    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),  # 1s, 2s, 4s
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True
    )
    async def _send_http_request(
        client: httpx.AsyncClient,
        webhook_url: str,
        payload: dict
    ) -> httpx.Response:
        """
        Send HTTP request with automatic retry on timeout or 5xx errors.
        
        Retry strategy:
        - Attempt 1: Immediate
        - Attempt 2: Wait 1s
        - Attempt 3: Wait 2s
        - Attempt 4: Wait 4s (total 3 retries)
        """
        response = await client.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5.0  # 5-second timeout
        )
        
        # Raise exception for 5xx errors to trigger retry
        if response.status_code >= 500:
            response.raise_for_status()
        
        return response
    
    @staticmethod
    async def send_webhook(
        db: AsyncSession,
        webhook_url: str,
        event_type: str,
        interaction: Interaction,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send webhook notification with enterprise-grade reliability.
        
        Features:
        - Automatic retry with exponential backoff
        - Structured logging with latency tracking
        - Failed webhook persistence
        
        Args:
            db: Database session
            webhook_url: The webhook endpoint URL
            event_type: Type of event (appointment.created, etc.)
            interaction: The interaction object (replacing appointment)
            additional_data: Any additional data to send
            
        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()
        
        # Prepare payload
        payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "tenant_id": str(interaction.tenant_id),
            "data": {
                "appointment_id": str(interaction.id), # Keeping key for backward compatibility or rename to interaction_id
                "interaction_id": str(interaction.id),
                "title": interaction.title,
                "description": interaction.description,
                "start_time": interaction.start_time.isoformat(),
                "end_time": interaction.end_time.isoformat(),
                "client": {
                    "name": interaction.client_name,
                    "email": interaction.client_email,
                    "phone": interaction.client_phone
                },
                "status": interaction.status.value,
                "created_at": interaction.created_at.isoformat(),
                "updated_at": interaction.updated_at.isoformat(),
            }
        }
        
        if additional_data:
            payload["data"].update(additional_data)
        
        attempt_count = 0
        last_error = None
        last_status_code = None
        
        try:
            async with httpx.AsyncClient() as client:
                # Attempt with automatic retry
                response = await WebhookService._send_http_request(
                    client, webhook_url, payload
                )
                
                latency_ms = (time.time() - start_time) * 1000
                
                # Success!
                logger.info(
                    "webhook_sent_successfully",
                    event_type=event_type,
                    webhook_url=webhook_url,
                    status_code=response.status_code,
                    latency_ms=round(latency_ms, 2),
                    tenant_id=str(interaction.tenant_id),
                    appointment_id=str(interaction.id)
                )
                
                return True
                
        except RetryError as e:
            # All retries exhausted
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract original exception
            original_exception = e.last_attempt.exception()
            
            if isinstance(original_exception, httpx.HTTPStatusError):
                last_error = f"HTTP {original_exception.response.status_code}: {original_exception.response.text[:200]}"
                last_status_code = original_exception.response.status_code
            elif isinstance(original_exception, httpx.TimeoutException):
                last_error = "Connection timeout after 5 seconds"
                last_status_code = 0
            else:
                last_error = str(original_exception)[:500]
                last_status_code = 0
            
            attempt_count = e.last_attempt.attempt_number
            
            logger.error(
                "webhook_failed_after_retries",
                event_type=event_type,
                webhook_url=webhook_url,
                error=last_error,
                status_code=last_status_code,
                attempts=attempt_count,
                latency_ms=round(latency_ms, 2),
                tenant_id=str(interaction.tenant_id),
                appointment_id=str(interaction.id)
            )
            
        except Exception as e:
            # Unexpected error
            latency_ms = (time.time() - start_time) * 1000
            last_error = str(e)[:500]
            attempt_count = 1
            
            logger.error(
                "webhook_unexpected_error",
                event_type=event_type,
                webhook_url=webhook_url,
                error=last_error,
                latency_ms=round(latency_ms, 2),
                tenant_id=str(interaction.tenant_id),
                appointment_id=str(interaction.id)
            )
        
        # Persist failed webhook for manual retry
        await WebhookService._save_failed_webhook(
            db=db,
            tenant_id=interaction.tenant_id,
            event_type=event_type,
            webhook_url=webhook_url,
            payload=payload,
            attempts=attempt_count,
            last_error=last_error,
            last_status_code=last_status_code,
            related_entity_type="appointment",
            related_entity_id=str(interaction.id)
        )
        
        return False
    
    @staticmethod
    async def _save_failed_webhook(
        db: AsyncSession,
        tenant_id: UUID,
        event_type: str,
        webhook_url: str,
        payload: dict,
        attempts: int,
        last_error: Optional[str],
        last_status_code: Optional[int],
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None
    ):
        """
        Save failed webhook to database for manual retry.
        """
        failed_webhook = FailedWebhook(
            tenant_id=tenant_id,
            event_type=event_type,
            webhook_url=webhook_url,
            payload=payload,
            status=WebhookStatus.FAILED,
            attempts=attempts,
            last_error=last_error,
            last_status_code=last_status_code,
            last_attempt_at=datetime.utcnow(),
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id
        )
        
        db.add(failed_webhook)
        await db.commit()
        
        logger.info(
            "failed_webhook_saved",
            failed_webhook_id=str(failed_webhook.id),
            event_type=event_type,
            tenant_id=str(tenant_id)
        )
    
    @staticmethod
    async def notify_appointment_created(
        db: AsyncSession,
        interaction: Interaction,
        webhook_url: Optional[str] = None
    ) -> bool:
        """Notify external systems about new appointment."""
        if not webhook_url:
            return False
            
        return await WebhookService.send_webhook(
            db=db,
            webhook_url=webhook_url,
            event_type="appointment.created",
            interaction=interaction
        )
    
    @staticmethod
    async def notify_appointment_updated(
        db: AsyncSession,
        interaction: Interaction,
        webhook_url: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Notify external systems about appointment update."""
        if not webhook_url:
            return False
            
        additional_data = {"changes": changes} if changes else None
        
        return await WebhookService.send_webhook(
            db=db,
            webhook_url=webhook_url,
            event_type="appointment.updated",
            interaction=interaction,
            additional_data=additional_data
        )
    
    @staticmethod
    async def notify_appointment_cancelled(
        db: AsyncSession,
        interaction: Interaction,
        webhook_url: Optional[str] = None
    ) -> bool:
        """Notify external systems about appointment cancellation."""
        if not webhook_url:
            return False
            
        return await WebhookService.send_webhook(
            db=db,
            webhook_url=webhook_url,
            event_type="appointment.cancelled",
            interaction=interaction
        )
    
    @staticmethod
    async def retry_failed_webhook(
        db: AsyncSession,
        failed_webhook_id: UUID,
        retried_by: str
    ) -> bool:
        """
        Manually retry a failed webhook from admin panel.
        
        Args:
            db: Database session
            failed_webhook_id: ID of failed webhook
            retried_by: Username/ID of admin who triggered retry
            
        Returns:
            True if successful, False otherwise
        """
        from sqlalchemy import select
        
        # Get failed webhook
        query = select(FailedWebhook).where(FailedWebhook.id == failed_webhook_id)
        result = await db.execute(query)
        failed_webhook = result.scalar_one_or_none()
        
        if not failed_webhook:
            logger.error("failed_webhook_not_found", failed_webhook_id=str(failed_webhook_id))
            return False
        
        # Attempt to resend
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    failed_webhook.webhook_url,
                    json=failed_webhook.payload,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0
                )
                
                latency_ms = (time.time() - start_time) * 1000
                
                if response.status_code in [200, 201, 202, 204]:
                    # Success!
                    failed_webhook.status = WebhookStatus.MANUALLY_SENT
                    failed_webhook.manually_retried_at = datetime.utcnow()
                    failed_webhook.manually_retried_by = retried_by
                    
                    await db.commit()
                    
                    logger.info(
                        "failed_webhook_manually_retried_success",
                        failed_webhook_id=str(failed_webhook_id),
                        status_code=response.status_code,
                        latency_ms=round(latency_ms, 2),
                        retried_by=retried_by
                    )
                    
                    return True
                else:
                    logger.warning(
                        "failed_webhook_manual_retry_bad_status",
                        failed_webhook_id=str(failed_webhook_id),
                        status_code=response.status_code
                    )
                    return False
                    
        except Exception as e:
            logger.error(
                "failed_webhook_manual_retry_error",
                failed_webhook_id=str(failed_webhook_id),
                error=str(e),
                retried_by=retried_by
            )
            return False
