import json
import redis.asyncio as redis
import time
from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.customer import Customer
from app.models.tenant import Tenant
from app.schemas.vapi import (
    VapiWebhookRequest,
    VapiWebhookResponse,
    VapiAssistantConfig,
    VapiAssistantModel,
    VapiPerformanceLog
)


class VapiService:
    """
    Service layer for Vapi.ai webhook with Antigravity speed (millisecond response).
    
    Performance target: < 200ms response time
    Strategy: Redis cache-first for customer data
    """
    
    # Redis connection pool
    _redis_client: Optional[redis.Redis] = None
    
    # Performance threshold
    WARNING_THRESHOLD_MS = 200.0
    
    @classmethod
    async def get_redis_client(cls) -> redis.Redis:
        """Get or create Redis client."""
        if cls._redis_client is None:
            cls._redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True
            )
        return cls._redis_client
    
    @staticmethod
    def _get_customer_cache_key(tenant_id: UUID, phone: str) -> str:
        """Generate Redis cache key for customer."""
        return f"vapi:customer:{tenant_id}:{phone}"
    
    @staticmethod
    def _get_tenant_prompt_cache_key(tenant_id: UUID) -> str:
        """Generate Redis cache key for tenant system prompt."""
        return f"vapi:tenant:prompt:{tenant_id}"
    
    @staticmethod
    async def get_customer_segment_cached(
        db: AsyncSession,
        tenant_id: UUID,
        customer_number: str
    ) -> tuple[Optional[str], bool]:
        """
        Get customer segment with Redis cache-first strategy.
        
        Returns:
            (segment, redis_hit)
            - segment: Customer segment (VIP, GOLD, etc.) or None
            - redis_hit: True if found in Redis, False if DB query was needed
        """
        redis_client = await VapiService.get_redis_client()
        cache_key = VapiService._get_customer_cache_key(tenant_id, customer_number)
        
        # Step 1: Try Redis cache (FAST!)
        cached_segment = await redis_client.get(cache_key)
        
        if cached_segment:
            print(f"⚡ CACHE HIT: Customer segment from Redis: {cached_segment}")
            return cached_segment, True
        
        # Step 2: Cache miss - Query database
        print(f"💾 CACHE MISS: Querying database for customer: {customer_number}")
        
        query = select(Customer.segment).where(
            and_(
                Customer.tenant_id == tenant_id,
                Customer.phone == customer_number
            )
        )
        
        result = await db.execute(query)
        customer_segment = result.scalar_one_or_none()
        
        if customer_segment:
            # customer_segment is already the enum value (CustomerSegment enum)
            segment = customer_segment.value if hasattr(customer_segment, 'value') else str(customer_segment)
            
            # Step 3: Cache the result (TTL: 1 hour)
            await redis_client.setex(cache_key, 3600, segment)
            print(f"✅ Cached customer segment: {segment}")
            
            return segment, False
        
        # Customer not found
        return None, False
    
    @staticmethod
    async def get_tenant_system_prompt_cached(
        db: AsyncSession,
        tenant_id: UUID
    ) -> tuple[str, bool]:
        """
        Get tenant system prompt with Redis cache-first strategy.
        
        Returns:
            (system_prompt, redis_hit)
        """
        redis_client = await VapiService.get_redis_client()
        cache_key = VapiService._get_tenant_prompt_cache_key(tenant_id)
        
        # Step 1: Try Redis cache
        cached_prompt = await redis_client.get(cache_key)
        
        if cached_prompt:
            print(f"⚡ CACHE HIT: System prompt from Redis")
            return cached_prompt, True
        
        # Step 2: Cache miss - Query database
        print(f"💾 CACHE MISS: Querying database for tenant system prompt")
        
        query = select(Tenant).where(Tenant.id == tenant_id)
        result = await db.execute(query)
        tenant = result.scalar_one_or_none()
        
        if tenant:
            # Assume tenant has a system_prompt field
            # If not, we'll use a default
            system_prompt = getattr(tenant, 'system_prompt', VapiService._get_default_system_prompt())
            
            # Step 3: Cache the result (TTL: 24 hours - prompts change less frequently)
            await redis_client.setex(cache_key, 86400, system_prompt)
            print(f"✅ Cached system prompt")
            
            return system_prompt, False
        
        # Tenant not found - use default
        return VapiService._get_default_system_prompt(), False
    
    @staticmethod
    def _get_default_system_prompt() -> str:
        """Get default system prompt if tenant doesn't have one."""
        return """You are a helpful AI assistant for our company. 
Be professional, friendly, and helpful. 
Answer customer questions clearly and concisely.
If you don't know something, politely say so and offer to connect them with a human representative."""
    
    @staticmethod
    def _customize_prompt_for_segment(base_prompt: str, segment: Optional[str]) -> str:
        """Customize system prompt based on customer segment."""
        if not segment:
            return base_prompt
        
        segment_lower = segment.lower()
        
        if segment_lower == "vip":
            return base_prompt + """

IMPORTANT: This is a VIP customer. Provide premium service:
- Prioritize their requests
- Offer exclusive deals and benefits
- Be extra attentive and professional
- Escalate to senior staff if needed"""
        elif segment_lower == "gold":
            return base_prompt + """

NOTE: This is a GOLD tier customer. Provide priority service:
- Offer special discounts when applicable
- Be attentive to their needs
- Thank them for their loyalty"""
        else:
            return base_prompt

    @staticmethod
    async def get_customer_interaction_history(
        db: AsyncSession,
        tenant_id: UUID,
        customer_number: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent interactions for the customer to build context.
        """
        # We need to import Interaction dynamically or at top if checking circular imports
        from app.models.interaction import Interaction
        
        # Find customer by phone to get name if possible, though customer_number is key
        # Assuming customer_number matches client_phone or we look up Customer first
        
        query = select(Interaction).where(
            and_(
                Interaction.tenant_id == tenant_id,
                # Simple phone match for now, ideally normalize phone numbers
                Interaction.client_phone == customer_number
            )
        ).order_by(Interaction.start_time.desc()).limit(limit)
        
        result = await db.execute(query)
        interactions = result.scalars().all()
        
        history = []
        for interaction in interactions:
            history.append({
                "type": interaction.type,
                "title": interaction.title,
                "date": interaction.start_time.strftime("%Y-%m-%d"),
                "status": interaction.status.value
            })
            
        return history

    @staticmethod
    async def generate_contextual_prompt(
        base_prompt: str, 
        segment: Optional[str],
        history: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a highly contextual system prompt.
        """
        # 1. Segment Customization
        contextual_prompt = VapiService._customize_prompt_for_segment(base_prompt, segment)
        
        # 2. History Injection
        if history:
            history_text = "\n".join([
                f"- {h['date']}: {h['title']} ({h['status']})" for h in history
            ])
            
            contextual_prompt += f"""
            
CONTEXT - RECENT INTERACTIONS:
The customer has the following recent history with us:
{history_text}

INSTRUCTION:
Use this history to greet the customer warmly and show we remember them. 
Example: "I see you visited us on {history[0]['date']} for {history[0]['title']}. How is everything going with that?"
Do not be creepy, just helpful and attentive.
"""
        
        return contextual_prompt

    @staticmethod
    async def process_vapi_webhook(
        db: AsyncSession,
        tenant_id: UUID,
        request: VapiWebhookRequest
    ) -> tuple[VapiWebhookResponse, VapiPerformanceLog]:
        """
        Process Vapi webhook with Antigravity speed.
        """
        start_time = time.time()
        
        # Step 1: Get customer segment (Redis-first)
        segment, redis_hit_customer = await VapiService.get_customer_segment_cached(
            db=db,
            tenant_id=tenant_id,
            customer_number=request.customer_number
        )
        
        # Step 2: Get tenant system prompt (Redis-first)
        base_prompt, redis_hit_prompt = await VapiService.get_tenant_system_prompt_cached(
            db=db,
            tenant_id=tenant_id
        )
        
        # Step 3: Get Customer History (Database - fast query)
        history = await VapiService.get_customer_interaction_history(
            db=db,
            tenant_id=tenant_id,
            customer_number=request.customer_number
        )
        
        # Step 4: Generate Contextual Prompt
        customized_prompt = await VapiService.generate_contextual_prompt(base_prompt, segment, history)
        
        # Step 5: Build Vapi response
        first_message = f"Hello! How can I assist you today?"
        
        # Personalized first message if history exists
        if history:
            last_interaction = history[0]
            first_message = f"Hello! Welcome back. I see you had a {last_interaction['title']} on {last_interaction['date']}. How can I help you today?"
        elif segment and segment.lower() == "vip":
            first_message = "Hello! Welcome back, valued customer. How may I provide you with premium assistance today?"

        assistant_config = VapiAssistantConfig(
            model=VapiAssistantModel(
                provider="openai",
                model="gpt-4",
                temperature=0.7,
                max_tokens=500
            ),
            systemPrompt=customized_prompt,
            firstMessage=first_message
        )
        
        response = VapiWebhookResponse(assistant=assistant_config)
        
        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000
        
        # Performance logging
        warning = None
        if response_time_ms > VapiService.WARNING_THRESHOLD_MS:
            warning = f"⚠️ SLOW RESPONSE: {response_time_ms:.2f}ms (threshold: {VapiService.WARNING_THRESHOLD_MS}ms)"
            print(warning)
        else:
            print(f"✅ FAST RESPONSE: {response_time_ms:.2f}ms (Antigravity speed!)")
        
        performance_log = VapiPerformanceLog(
            call_id=request.call_id or "unknown",
            customer_number=request.customer_number,
            customer_segment=segment,
            redis_hit=redis_hit_customer and redis_hit_prompt,
            response_time_ms=round(response_time_ms, 2),
            warning=warning
        )
        
        return response, performance_log
