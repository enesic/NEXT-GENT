import asyncio
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
import time

from app.schemas.message import (
    IncomingWebhookMessage,
    OutgoingWebhookMessage,
    MessageResponse,
    MessageIntent
)
# Service integrations - ready for when services are implemented
# from app.services.appointment_service import AppointmentService
# from app.services.customer_service import CustomerService


class MessageService:
    """
    Service layer for message processing with retry logic and background tasks.
    """
    
    @staticmethod
    async def send_message_with_retry(
        webhook_url: str,
        message: OutgoingWebhookMessage,
        max_retries: int = 3,
        initial_delay: float = 1.0
    ) -> bool:
        """
        Send message with exponential backoff retry logic.
        
        Retry strategy:
        - Attempt 1: Immediate
        - Attempt 2: Wait 1 second
        - Attempt 3: Wait 2 seconds (exponential backoff)
        - Attempt 4: Wait 4 seconds
        
        Args:
            webhook_url: Target webhook URL
            message: Message to send
            max_retries: Maximum number of retry attempts (default: 3)
            initial_delay: Initial delay in seconds (default: 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        delay = initial_delay
        
        for attempt in range(max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        webhook_url,
                        json=message.model_dump(mode='json'),
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code in [200, 201, 202, 204]:
                        if attempt > 0:
                            print(f"✅ Message sent successfully on attempt {attempt + 1}")
                        return True
                    else:
                        print(f"❌ Attempt {attempt + 1} failed with status {response.status_code}")
                        
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                print(f"❌ Attempt {attempt + 1} failed: {type(e).__name__}")
                
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed with unexpected error: {str(e)}")
            
            # Don't wait after the last attempt
            if attempt < max_retries:
                print(f"⏳ Waiting {delay:.1f}s before retry...")
                await asyncio.sleep(delay)
                # Exponential backoff: double the delay
                delay *= 2
        
        print(f"❌ All {max_retries + 1} attempts failed")
        return False
    
    @staticmethod
    async def process_incoming_message(
        message: IncomingWebhookMessage
    ) -> MessageResponse:
        """
        Process incoming webhook message based on intent.
        
        Intent routing:
        - randevu_olustur → Create appointment
        - randevu_iptal → Cancel appointment
        - musteri_bilgi → Get customer info
        - fallback → Generic response
        
        Args:
            message: Incoming webhook message
            
        Returns:
            MessageResponse with processing result
        """
        start_time = time.time()
        
        intent = MessageIntent(message.intent)
        
        # Route based on intent
        if intent == MessageIntent.APPOINTMENT_CREATE:
            response_message = await MessageService._handle_appointment_create(message)
            
        elif intent == MessageIntent.APPOINTMENT_CANCEL:
            response_message = await MessageService._handle_appointment_cancel(message)
            
        elif intent == MessageIntent.CUSTOMER_INFO:
            response_message = await MessageService._handle_customer_info(message)
            
        elif intent == MessageIntent.FALLBACK:
            response_message = "Üzgünüm, sizi anlayamadım. Lütfen daha açık bir şekilde belirtir misiniz?"
            
        else:
            response_message = "Bilinmeyen istek. Lütfen 'randevu oluştur', 'randevu iptal' veya 'müşteri bilgi' diyebilirsiniz."
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return MessageResponse(
            call_id=message.call_id,
            intent=intent,
            response_message=response_message,
            success=True,
            processing_time_ms=processing_time
        )
    
    @staticmethod
    async def _handle_appointment_create(message: IncomingWebhookMessage) -> str:
        """
        Handle appointment creation intent.
        
        Integrates with AppointmentService when available.
        """
        if not message.date or not message.time:
            return "Randevu oluşturmak için tarih ve saat bilgisi gereklidir. Örnek: 'Yarın saat 10:00'da randevu almak istiyorum.'"
        
        # READY FOR INTEGRATION: Uncomment when AppointmentService is available
        # try:
        #     appointment = await AppointmentService.create_appointment(
        #         customer_phone=message.phone,
        #         date=message.date,
        #         time=message.time,
        #         customer_name=message.name
        #     )
        #     return f"Randevunuz {appointment.date} tarihinde {appointment.time} saatinde oluşturuldu. Randevu No: {appointment.id}"
        # except Exception as e:
        #     return f"Randevu oluşturulurken bir hata oluştu: {str(e)}"
        
        return f"Randevunuz {message.date} tarihinde {message.time} saatinde oluşturuldu. Teşekkür ederiz!"
    
    @staticmethod
    async def _handle_appointment_cancel(message: IncomingWebhookMessage) -> str:
        """
        Handle appointment cancellation intent.
        
        Integrates with AppointmentService when available.
        """
        # READY FOR INTEGRATION: Uncomment when AppointmentService is available
        # try:
        #     await AppointmentService.cancel_appointment(
        #         customer_phone=message.phone,
        #         call_id=message.call_id
        #     )
        #     return "Randevunuz başarıyla iptal edildi. Başka bir konuda yardımcı olabilir miyim?"
        # except Exception as e:
        #     return f"Randevu iptal edilirken bir hata oluştu: {str(e)}"
        
        return "Randevunuz iptal edildi. Başka bir konuda yardımcı olabilir miyim?"
    
    @staticmethod
    async def _handle_customer_info(message: IncomingWebhookMessage) -> str:
        """
        Handle customer info request intent.
        
        Integrates with CustomerService when available.
        """
        if not message.phone:
            return "Müşteri bilgisi için telefon numarası gereklidir."
        
        # READY FOR INTEGRATION: Uncomment when CustomerService is available
        # try:
        #     customer = await CustomerService.get_customer_by_phone(message.phone)
        #     if customer:
        #         return f"Müşteri Adı: {customer.name}\nTelefon: {customer.phone}\nSegment: {customer.segment}"
        #     else:
        #         return "Bu telefon numarası ile kayıtlı müşteri bulunamadı."
        # except Exception as e:
        #     return f"Müşteri bilgisi alınırken bir hata oluştu: {str(e)}"
        
        return f"Müşteri bilgileriniz: {message.name or 'Bilinmiyor'}"
    
    @staticmethod
    async def send_response_background(
        webhook_url: str,
        call_id: str,
        response_message: str,
        intent: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Send response message in background with retry logic.
        
        This method is designed to be called with BackgroundTasks.
        """
        outgoing_message = OutgoingWebhookMessage(
            call_id=call_id,
            message=response_message,
            intent=intent,
            success=True,
            data=data
        )
        
        success = await MessageService.send_message_with_retry(
            webhook_url=webhook_url,
            message=outgoing_message,
            max_retries=3,
            initial_delay=1.0
        )
        
        if success:
            print(f"✅ Background response sent for call_id: {call_id}")
        else:
            print(f"❌ Failed to send background response for call_id: {call_id}")
