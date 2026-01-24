"""
AI Helpdesk endpoint for customer support.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.logger import get_logger
from app.core.websocket import manager
from app.models.tenant import Tenant

router = APIRouter()
logger = get_logger(__name__)


class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[list[str]] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    AI-powered helpdesk chat endpoint with automatic action execution.
    Processes customer questions, detects intent, and automatically performs actions.
    """
    try:
        from app.services.ai_service import AIService
        from app.services.function_calling_service import FunctionCallingService
        
        # Step 1: Detect intent using AI
        intent_result = await AIService.detect_intent(request.message)
        detected_intent = intent_result.get("intent")
        entities = intent_result.get("entities", {})
        confidence = intent_result.get("confidence", 0.5)
        
        # Step 2: If high confidence and actionable intent, execute function
        ai_response = None
        action_taken = False
        
        if confidence > 0.8 and detected_intent in ["appointment_create", "appointment_cancel", "customer_info"]:
            try:
                # Prepare function parameters
                if detected_intent == "appointment_create":
                    function_result = await FunctionCallingService.execute_function(
                        function_name="create_appointment",
                        parameters={
                            "title": entities.get("reason", "Appointment"),
                            "date": entities.get("date"),
                            "time": entities.get("time"),
                            "customer_name": entities.get("customer_name", "Customer"),
                            "customer_phone": entities.get("customer_phone", ""),
                            "customer_email": entities.get("customer_email", ""),
                            "type": "appointment"
                        },
                        context={
                            "db": db,
                            "tenant_id": current_tenant.id if current_tenant else (request.context.get("tenant_id") if request.context else None)
                        }
                    )
                    
                    if function_result.get("success"):
                        ai_response = function_result.get("result", {}).get("message", "Randevunuz oluşturuldu.")
                        action_taken = True
                
                elif detected_intent == "appointment_cancel":
                    function_result = await FunctionCallingService.execute_function(
                        function_name="cancel_appointment",
                        parameters={
                            "appointment_id": entities.get("appointment_id"),
                            "reason": entities.get("reason", "Customer request")
                        },
                        context={
                            "db": db,
                            "tenant_id": current_tenant.id if current_tenant else (request.context.get("tenant_id") if request.context else None)
                        }
                    )
                    
                    if function_result.get("success"):
                        ai_response = function_result.get("result", {}).get("message", "Randevunuz iptal edildi.")
                        action_taken = True
                
                elif detected_intent == "customer_info":
                    function_result = await FunctionCallingService.execute_function(
                        function_name="get_customer_info",
                        parameters={
                            "phone": entities.get("customer_phone"),
                            "email": entities.get("customer_email")
                        },
                        context={
                            "db": db,
                            "tenant_id": current_tenant.id if current_tenant else (request.context.get("tenant_id") if request.context else None)
                        }
                    )
                    
                    if function_result.get("success") and function_result.get("result", {}).get("found"):
                        customer = function_result.get("result", {}).get("customer", {})
                        ai_response = f"Müşteri bilgileri: {customer.get('name')}, Segment: {customer.get('segment')}, Durum: {customer.get('status')}"
                        action_taken = True
                
            except Exception as e:
                logger.error("function_execution_error", error=str(e), intent=detected_intent)
                # Continue to generate response even if function fails
        
        # Step 3: If no action taken, generate AI response
        if not ai_response:
            ai_response = await generate_ai_response(request.message, request.context)
        
        # Step 4: Send notification to admin in background
        background_tasks.add_task(
            notify_admin,
            message=request.message,
            response=ai_response,
            context=request.context,
            intent=detected_intent,
            action_taken=action_taken
        )
        
        return ChatResponse(
            response=ai_response,
            suggestions=get_suggestions(request.message)
        )
        
    except Exception as e:
        logger.error("helpdesk_chat_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI yardımcı şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin."
        )


async def generate_ai_response(message: str, context: Optional[Dict[str, Any]]) -> str:
    """
    Generate AI response using OpenAI (if available) or fallback to rule-based.
    """
    from app.services.ai_service import AIService
    
    # Try AI first
    try:
        ai_response = await AIService.generate_response(
            message=message,
            context=context,
            system_prompt="""You are a helpful AI assistant for NextGent customer support.
Be professional, friendly, and helpful. Answer questions clearly and concisely.
If you can help with appointments, customer info, or technical support, do so.
If you don't know something, politely say so and offer to connect them with a human representative."""
        )
        return ai_response
    except Exception as e:
        logger.warning("ai_response_failed", error=str(e), falling_back=True)
    
    # Fallback to rule-based
    message_lower = message.lower()
    
    # Greeting
    if any(word in message_lower for word in ['merhaba', 'selam', 'hello', 'hi']):
        return """Merhaba! 👋 NextGent AI Yardım Merkezi'ne hoş geldiniz. 

Size nasıl yardımcı olabilirim? Şunlar hakkında bilgi verebilirim:
• Ürün özellikleri ve fiyatlandırma
• Teknik destek
• Hesap yönetimi
• Entegrasyonlar

Hangi konuda yardıma ihtiyacınız var?"""
    
    # Pricing
    if any(word in message_lower for word in ['fiyat', 'ücret', 'maliyet', 'price', 'cost']):
        return """💼 **Fiyatlandırma Bilgileri**

NextGent, işletmenizin ihtiyaçlarına göre özelleştirilmiş fiyatlandırma sunar:

• **Starter Plan**: Aylık $99 - Temel özellikler
• **Professional Plan**: Aylık $299 - Gelişmiş analitik
• **Enterprise Plan**: Özel fiyatlandırma - Tam özelleştirme

Detaylı bilgi için lütfen bizimle iletişime geçin: sales@nextgent.com

Size özel bir teklif hazırlayabiliriz! 🚀"""
    
    # Features
    if any(word in message_lower for word in ['özellik', 'feature', 'ne yapabilir', 'neler var']):
        return """✨ **NextGent Özellikleri**

🚀 **Ana Özellikler:**
• AI Sesli Asistan (7/24 müşteri desteği)
• Gerçek Zamanlı Analitik Dashboard
• Multi-Tenant SaaS Mimarisi
• KVKK/GDPR Uyumlu Güvenlik
• Webhook Entegrasyonları (n8n, Zapier)
• Otomatik Müşteri Segmentasyonu

📊 **Analitik:**
• Canlı performans metrikleri
• Müşteri davranış analizi
• Gelir tahminleri
• AI destekli öneriler

🔒 **Güvenlik:**
• End-to-end şifreleme
• PII masking
• Role-based access control

Daha fazla bilgi için: https://nextgent.com/features"""
    
    # Support
    if any(word in message_lower for word in ['destek', 'yardım', 'sorun', 'problem', 'hata', 'support', 'help', 'issue']):
        return """🛟 **Teknik Destek**

Size yardımcı olmak için buradayız!

**Hızlı Çözümler:**
• Dokümantasyon: https://docs.nextgent.com
• Video Rehberler: https://nextgent.com/videos
• SSS: https://nextgent.com/faq

**İletişim:**
• Email: support@nextgent.com
• Telefon: +90 (XXX) XXX XX XX
• Canlı Destek: Hafta içi 09:00-18:00

Sorununuzu detaylı açıklarsanız, size daha hızlı yardımcı olabiliriz! 📧"""
    
    # Demo
    if any(word in message_lower for word in ['demo', 'deneme', 'test', 'trial']):
        return """🎬 **Demo ve Deneme**

NextGent'i ücretsiz deneyebilirsiniz!

**14 Günlük Ücretsiz Deneme:**
• Tüm özelliklere erişim
• Kredi kartı gerekmez
• Anında başlangıç

**Demo Talep Et:**
1. "Hemen Başlayın" butonuna tıklayın
2. Hesabınızı oluşturun
3. 14 gün boyunca ücretsiz kullanın

**Canlı Demo:**
• Salı ve Perşembe: 14:00-15:00
• Kayıt: https://nextgent.com/demo

Sorularınız için: demo@nextgent.com"""
    
    # Default response
    return f"""Teşekkürler! Mesajınızı aldım: "{message}"

Size en iyi şekilde yardımcı olabilmem için şu konularda bilgi verebilirim:

💼 **Fiyatlandırma ve Planlar**
✨ **Özellikler ve Yetenekler**
🛟 **Teknik Destek**
🎬 **Demo ve Deneme**

Hangi konuda yardıma ihtiyacınız var? Veya daha detaylı bilgi için bizimle iletişime geçebilirsiniz: support@nextgent.com"""
    
    # Note: In production, replace this with actual AI API call:
    # response = await openai_client.chat.completions.create(...)


def get_suggestions(message: str) -> list[str]:
    """Get suggested follow-up questions."""
    message_lower = message.lower()
    
    if 'fiyat' in message_lower:
        return ["Özelleştirilmiş teklif almak istiyorum", "Enterprise plan hakkında bilgi"]
    elif 'özellik' in message_lower:
        return ["AI asistan nasıl çalışır?", "Analitik özellikleri neler?"]
    else:
        return ["Fiyatlandırma bilgisi", "Özellikler hakkında bilgi", "Demo talep et"]


async def notify_admin(
    message: str, 
    response: str, 
    context: Optional[Dict[str, Any]],
    intent: Optional[str] = None,
    action_taken: bool = False
):
    """
    Send notification to admin about new helpdesk interaction.
    This can be sent via WebSocket, email, or other channels.
    """
    try:
        from app.core.websocket import manager
        
        # Broadcast to all admin users via WebSocket
        # In production, filter by admin tenant IDs
        notification = {
            "type": "HELPDESK_MESSAGE",
            "data": {
                "message": message,
                "response": response,
                "context": context,
                "intent": intent,
                "action_taken": action_taken,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        # Log notification
        logger.info(
            "helpdesk_notification",
            message=message[:100],  # Truncate for logging
            response_length=len(response),
            intent=intent,
            action_taken=action_taken,
            context=context
        )
        
        # Broadcast via WebSocket (if tenant_id available in context)
        if context and context.get("tenant_id"):
            try:
                await manager.broadcast_to_tenant(
                    str(context["tenant_id"]),
                    notification
                )
            except Exception as e:
                logger.warning("websocket_broadcast_failed", error=str(e))
        
    except Exception as e:
        logger.error("helpdesk_notification_error", error=str(e))


