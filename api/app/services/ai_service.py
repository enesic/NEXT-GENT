"""
AI Service - OpenAI/Claude integration for intelligent responses.
"""
import os
import json
import time
import asyncio
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, RateLimitError
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client
ai_client: Optional[AsyncOpenAI] = None

# Simple in-memory cache for intent detection to save costs and latency
# Key: message string, Value: (timestamp, result_dict)
_intent_cache: Dict[str, Any] = {}
CACHE_TTL = 3600  # 1 hour

def get_ai_client() -> AsyncOpenAI:
    """Get or create OpenAI client."""
    global ai_client
    if ai_client is None:
        api_key = os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)
        if not api_key:
            logger.warning("OPENAI_API_KEY not set, AI features will use fallback")
            return None
        ai_client = AsyncOpenAI(api_key=api_key)
    return ai_client

async def _retry_operation(operation, max_retries=3, delay=1.0):
    """Retry an async operation with exponential backoff."""
    last_exception = None
    for i in range(max_retries):
        try:
            return await operation()
        except (APITimeoutError, APIConnectionError, RateLimitError) as e:
            last_exception = e
            wait_time = delay * (2 ** i)
            logger.warning(f"AI operation failed (attempt {i+1}/{max_retries}), retrying in {wait_time}s...", error=str(e))
            await asyncio.sleep(wait_time)
        except Exception as e:
            # Don't retry other errors (like 400 Bad Request)
            raise e
    raise last_exception

class AIService:
    """
    AI Service for intelligent responses, intent detection, and sentiment analysis.
    """
    
    @staticmethod
    async def generate_response(
        message: str,
        context: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate AI response using OpenAI GPT-4.
        """
        client = get_ai_client()
        if not client:
            return await AIService._fallback_response(message)
        
        try:
            messages = []
            
            # System Prompt
            default_system = """You are a helpful AI assistant for NextGent, a next-generation Customer Relationship Management (CRM) platform tailored for enterprises.

Your goal is to assist potential and existing customers by providing accurate information about NextGent's products, services, pricing, and features.

**About NextGent:**
NextGent is an AI-powered CRM designed to revolutionize customer interactions. We specialize in bringing AI voice assistants, real-time analytics, and secure data management to various sectors.

**Key Features:**
- **AI Voice Assistant:** 24/7 intelligent voice support that handles calls, schedules appointments, and answers queries naturally.
- **Real-Time Analytics:** Live dashboards providing actionable insights into customer behavior and operational efficiency.
- **KVKK & GDPR Compliance:** Enterprise-grade security with end-to-end encryption for all sensitive data (PII).
- **Multi-Tenant Architecture:** Scalable and secure environment for managing multiple branches or clients.
- **Sector-Specific Modules:** Tailored solutions for Medical, Legal, Real Estate, Finance, and more.

**Pricing Tiers:**
1. **Starter Plan ($99/month):** Best for small businesses. Includes basic CRM, email support, and 1 AI voice agent.
2. **Professional Plan ($299/month):** For growing teams. Includes advanced analytics, priority support, and 3 AI voice agents.
3. **Enterprise Plan (Custom):** For large organizations. Unlimited AI agents, dedicated account manager, API access, and on-premise deployment options.

**Contact & Support:**
- **Sales:** sales@nextgent.com or +90 (212) 555 0100
- **Support:** support@nextgent.com
- **Website:** www.nextgent.com
- **Demo:** You can request a live demo via our website.

**Guidelines:**
- Be professional, friendly, and concise.
- Use emojis sparingly to sound approachable but professional.
- If unsure about a detail, do not make it up. Direct the user to support@nextgent.com.
- Always answer in the language the user speaks (mainly Turkish or English).
"""
            
            messages.append({
                "role": "system",
                "content": system_prompt or default_system
            })
            
            # Context
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Context: {json.dumps(context, default=str)}"
                })
            
            # User Message
            messages.append({
                "role": "user",
                "content": message
            })
            
            async def _call_api():
                response = await client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content

            return await _retry_operation(_call_api)
            
        except Exception as e:
            logger.error("ai_response_error", error=str(e))
            return await AIService._fallback_response(message)
    
    @staticmethod
    async def detect_intent(
        message: str,
        available_functions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Detect user intent using AI with caching.
        """
        # Check cache
        cache_key = message.strip().lower()
        if cache_key in _intent_cache:
            timestamp, cached_result = _intent_cache[cache_key]
            if time.time() - timestamp < CACHE_TTL:
                logger.debug("intent_detection_cache_hit", message=message)
                return cached_result
            else:
                del _intent_cache[cache_key]

        client = get_ai_client()
        if not client:
            return await AIService._fallback_intent_detection(message)
        
        try:
            functions = [
                {
                    "type": "function",
                    "function": {
                        "name": "detect_intent",
                        "description": "Detect user intent from message",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "intent": {
                                    "type": "string",
                                    "enum": [
                                        "appointment_create",
                                        "appointment_cancel",
                                        "appointment_reschedule",
                                        "customer_info",
                                        "satisfaction_feedback",
                                        "general_inquiry",
                                        "technical_support"
                                    ],
                                    "description": "Detected intent"
                                },
                                "confidence": {
                                    "type": "number",
                                    "description": "Confidence score 0-1"
                                },
                                "entities": {
                                    "type": "object",
                                    "properties": {
                                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                                        "time": {"type": "string", "description": "Time in HH:MM format"},
                                        "customer_name": {"type": "string"},
                                        "customer_phone": {"type": "string"},
                                        "reason": {"type": "string", "description": "Reason for cancellation or inquiry"}
                                    }
                                }
                            },
                            "required": ["intent", "confidence"]
                        }
                    }
                }
            ]
            
            async def _call_api():
                return await client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an intent detection system. Analyze user messages and detect their intent accurately."},
                        {"role": "user", "content": message}
                    ],
                    tools=functions,
                    tool_choice={"type": "function", "function": {"name": "detect_intent"}},
                    temperature=0.0  # Zero temperature for deterministic results
                )

            response = await _retry_operation(_call_api)
            
            tool_call = response.choices[0].message.tool_calls[0] if response.choices[0].message.tool_calls else None
            result = None
            
            if tool_call:
                result = json.loads(tool_call.function.arguments)
            else:
                result = await AIService._fallback_intent_detection(message)
            
            # Cache the result
            _intent_cache[cache_key] = (time.time(), result)
            return result
            
        except Exception as e:
            logger.error("intent_detection_error", error=str(e))
            return await AIService._fallback_intent_detection(message)
    
    @staticmethod
    async def analyze_sentiment(
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of text using AI.
        """
        client = get_ai_client()
        if not client:
            return AIService._fallback_sentiment(text)
        
        try:
            prompt = f"""Analyze the sentiment of this text and provide:
1. Sentiment: positive, neutral, or negative
2. Score: 0.0 to 1.0 (1.0 = very positive, 0.0 = very negative)
3. Emotions: list of emotions detected
4. Summary: brief summary

Text: {text}
{f'Context: {context}' if context else ''}

Respond in JSON format."""
            
            async def _call_api():
                return await client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a sentiment analysis expert. Respond in valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
            
            response = await _retry_operation(_call_api)
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error("sentiment_analysis_error", error=str(e))
            return AIService._fallback_sentiment(text)
    
    @staticmethod
    async def call_function(
        function_name: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Call a system function using AI function calling.
        """
        logger.info("function_call_requested", function=function_name, parameters=parameters)
        from app.services.function_calling_service import FunctionCallingService
        return await FunctionCallingService.execute_function(
            function_name=function_name,
            parameters=parameters,
            context=context
        )
    
    # Fallback methods
    @staticmethod
    async def _fallback_response(message: str) -> str:
        """Fallback response when AI is not available."""
        message_lower = message.lower()
        if any(word in message_lower for word in ['merhaba', 'selam', 'hello']):
            return "Merhaba! Size nasıl yardımcı olabilirim?"
        elif any(word in message_lower for word in ['randevu', 'appointment']):
            return "Randevu oluşturmak için lütfen tarih ve saat belirtin."
        else:
            return "Anladım. Size yardımcı olmak için daha fazla bilgi verebilir misiniz?"
    
    @staticmethod
    async def _fallback_intent_detection(message: str) -> Dict[str, Any]:
        """Fallback intent detection using keywords."""
        message_lower = message.lower()
        if any(word in message_lower for word in ['randevu', 'appointment', 'rezervasyon']):
            if any(word in message_lower for word in ['iptal', 'cancel']):
                return {"intent": "appointment_cancel", "confidence": 0.7, "entities": {}}
            else:
                return {"intent": "appointment_create", "confidence": 0.7, "entities": {}}
        elif any(word in message_lower for word in ['müşteri', 'customer', 'bilgi', 'info']):
            return {"intent": "customer_info", "confidence": 0.7, "entities": {}}
        else:
            return {"intent": "general_inquiry", "confidence": 0.5, "entities": {}}
    
    @staticmethod
    def _fallback_sentiment(text: str) -> Dict[str, Any]:
        """Fallback sentiment analysis using keywords."""
        text_lower = text.lower()
        positive_words = ['iyi', 'güzel', 'mükemmel', 'harika', 'teşekkür', 'good', 'great', 'excellent']
        negative_words = ['kötü', 'berbat', 'şikayet', 'problem', 'sorun', 'bad', 'terrible', 'complaint']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(0.7 + (positive_count * 0.1), 1.0)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = max(0.3 - (negative_count * 0.1), 0.0)
        else:
            sentiment = "neutral"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": score,
            "emotions": [],
            "summary": f"Detected {sentiment} sentiment"
        }
