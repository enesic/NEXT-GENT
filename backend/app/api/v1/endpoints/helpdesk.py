"""
AI Helpdesk endpoint for customer support.
"""
from typing import Dict, Any, Optional, List
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
    suggestions: Optional[List[str]] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    """
    AI-powered helpdesk chat endpoint.
    Public endpoint - No authentication required.
    """
    try:
        logger.info(f"Helpdesk Chat Request: {request.message[:50]}...")
        
        # Import here to avoid circular dependencies
        from app.services.ml_service import get_ml_service
        
        # Step 1: Use ML service
        try:
            ml_service = get_ml_service()
            ml_result = ml_service.process_message(request.message)
        except Exception as ml_error:
            logger.error(f"ML Service Failed: {str(ml_error)}")
            # Fallback if ML service fails completely
            return ChatResponse(
                response="Üzgünüm, şu anda sistemde bir yoğunluk var. Lütfen support@nextgent.com ile iletişime geçin.",
                suggestions=["Teknik Destek", "İletişim"]
            )
            
        intent = ml_result.get("intent")
        confidence = ml_result.get("confidence", 0.0)
        ai_response = ml_result.get("response")
        suggestions = ml_result.get("suggestions", [])
        
        logger.info(f"Response Generated: Intent={intent}, Confidence={confidence}")
        
        # Step 2: Send notification (Wrapped in try/except to prevent 500)
        try:
            # Uncomment when stable
            # background_tasks.add_task(
            #     notify_admin,
            #     message=request.message,
            #     response=ai_response,
            #     context=request.context,
            #     intent=intent,
            #     action_taken=False
            # )
            pass
        except Exception as bg_error:
            logger.error(f"Background Task Failed: {str(bg_error)}")
        
        return ChatResponse(
            response=ai_response,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error("helpdesk_chat_critical_error", error=str(e))
        # Print to stdout/stderr to be sure we see it in console
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sunucu hatası: {str(e)}"
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
            system_prompt="""You are the official AI Assistant for NextGent (Next Gen Technology).
Your goal is to provide **definitive, clear, and professional** answers in Turkish.
Company Info:
- **NextGent** is an AI-powered Operation System integrating Phone, WhatsApp, CRM, and Automation into one 24/7 platform.
- **Key Features**: Auto-scheduling, Real-time Analytics, KVKK/GDPR Compliance, Multi-tenant SaaS.
- **Sectors**: Health (Clinics), Legal (Law Firms), Real Estate.
- **Pricing**: Starter (2.999 TL/mo), Pro (5.999 TL/mo), Enterprise (Custom).
- **Contact**: support@nextgent.com.
- **Philosophy**: "Future Management with AI".
If you are unsure, offer to connect to a human agent immediately. Do not guess."""
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

• **Başlangıç Paketi**: 2.999 TL/ay
• **Profesyonel Paket**: 5.999 TL/ay
• **Enterprise**: Size özel teklif

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


