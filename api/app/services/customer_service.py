import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.customer import Customer, CustomerSegment, CustomerStatus
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerStatusCheck,
    CustomerSegmentationResult
)


class CustomerService:
    """
    Service layer for customer management with Redis caching.
    Implements customer recognition and CRM workflows.
    """
    
    # Redis connection pool
    _redis_client: Optional[redis.Redis] = None
    
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
    def _get_cache_key(tenant_id: UUID, phone: str) -> str:
        """
        Generate Redis cache key for customer.
        Format: tenant:{tenant_id}:customer:{phone}
        """
        return f"tenant:{tenant_id}:customer:{phone}"
    
    @staticmethod
    async def get_customer_by_phone(
        db: AsyncSession,
        tenant_id: UUID,
        phone: str,
        use_cache: bool = True
    ) -> tuple[Optional[Customer], bool]:
        """
        Get customer by phone number with Redis caching (Antigravity Speed).
        
        Workflow:
        1. Check Redis cache (if enabled)
        2. If HIT: Reconstruct Customer object from cache (NO DB QUERY!)
        3. If MISS: Query PostgreSQL and cache result
        
        Args:
            db: Database session
            tenant_id: Tenant ID
            phone: Phone number (normalized)
            use_cache: Whether to use Redis cache
            
        Returns:
            Tuple of (Customer object or None, cache_hit: bool)
        """
        import time
        start_time = time.time()
        
        cache_key = CustomerService._get_cache_key(tenant_id, phone)
        
        # Step 1: Check Redis cache
        if use_cache:
            redis_client = await CustomerService.get_redis_client()
            cached_data = await redis_client.get(cache_key)
            
            if cached_data:
                # ✅ CACHE HIT - Reconstruct from cache (NO DB QUERY!)
                elapsed_ms = (time.time() - start_time) * 1000
                
                try:
                    customer_dict = json.loads(cached_data)
                    
                    # Reconstruct Customer object from cached dict
                    customer = Customer(
                        id=UUID(customer_dict["id"]),
                        tenant_id=UUID(customer_dict["tenant_id"]),
                        first_name=customer_dict["first_name"],
                        last_name=customer_dict["last_name"],
                        email=customer_dict["email"],
                        phone=customer_dict["phone"],
                        segment=CustomerSegment(customer_dict["segment"]),
                        status=CustomerStatus(customer_dict["status"]),
                        total_orders=customer_dict["total_orders"],
                        total_spent=customer_dict["total_spent"],
                        debt_amount=customer_dict["debt_amount"],
                        lifetime_value=customer_dict.get("lifetime_value", 0),
                        last_order_date=datetime.fromisoformat(customer_dict["last_order_date"]) if customer_dict.get("last_order_date") else None,
                        last_contact_date=datetime.fromisoformat(customer_dict["last_contact_date"]) if customer_dict.get("last_contact_date") else None,
                        created_at=datetime.fromisoformat(customer_dict["created_at"]),
                        updated_at=datetime.fromisoformat(customer_dict["updated_at"])
                    )
                    
                    # ⚡ Performance logging
                    print(f"⚡ CACHE HIT: {phone} | {elapsed_ms:.2f}ms | Antigravity speed!")
                    
                    return customer, True  # ✅ Cache HIT
                    
                except Exception as e:
                    # Cache data corrupted, fall through to DB query
                    print(f"⚠️  Cache data error: {e}, falling back to DB")
        
        # Step 2: Cache MISS - Query PostgreSQL
        elapsed_miss = (time.time() - start_time) * 1000
        print(f"❌ CACHE MISS: {phone} | {elapsed_miss:.2f}ms | Querying database...")
        
        query = select(Customer).where(
            and_(
                Customer.tenant_id == tenant_id,
                Customer.phone == phone
            )
        )
        
        result = await db.execute(query)
        customer = result.scalar_one_or_none()
        
        # Step 3: Cache the result in Redis (TTL: 1 hour)
        if customer and use_cache:
            redis_client = await CustomerService.get_redis_client()
            customer_dict = {
                "id": str(customer.id),
                "tenant_id": str(customer.tenant_id),
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "segment": customer.segment.value,
                "status": customer.status.value,
                "total_orders": customer.total_orders,
                "total_spent": float(customer.total_spent),
                "debt_amount": float(customer.debt_amount),
                "lifetime_value": float(customer.lifetime_value),
                "last_order_date": customer.last_order_date.isoformat() if customer.last_order_date else None,
                "last_contact_date": customer.last_contact_date.isoformat() if customer.last_contact_date else None,
                "created_at": customer.created_at.isoformat(),
                "updated_at": customer.updated_at.isoformat()
            }
            
            # Cache with 1 hour TTL
            await redis_client.setex(
                cache_key,
                3600,  # TTL: 1 hour
                json.dumps(customer_dict)
            )
            
            elapsed_total = (time.time() - start_time) * 1000
            print(f"✅ Cached customer: {phone} | Total: {elapsed_total:.2f}ms")
        
        return customer, False  # Cache MISS
    
    @staticmethod
    async def check_customer_status(
        db: AsyncSession,
        tenant_id: UUID,
        phone: str
    ) -> CustomerStatusCheck:
        """
        Check customer status with complex branching logic.
        
        Implements the workflow from image_e7d13a:
        - VIP customer check
        - Gold customer check
        - Debt check
        - Inactive customer check
        - Regular customer
        
        Returns detailed status and recommendation.
        """
        # Get customer (with cache)
        customer, cache_hit = await CustomerService.get_customer_by_phone(db, tenant_id, phone)
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Calculate days since last order
        days_since_last_order = None
        if customer.last_order_date:
            days_since_last_order = (datetime.utcnow() - customer.last_order_date).days
        
        # Status checks
        is_vip = customer.segment == CustomerSegment.VIP
        is_gold = customer.segment == CustomerSegment.GOLD
        has_debt = customer.debt_amount > 0
        is_inactive = days_since_last_order and days_since_last_order > 90
        is_blocked = customer.status == CustomerStatus.BLOCKED
        
        # Determine recommendation based on complex logic
        recommendation = CustomerService._determine_recommendation(
            is_vip=is_vip,
            is_gold=is_gold,
            has_debt=has_debt,
            is_inactive=is_inactive,
            is_blocked=is_blocked,
            debt_amount=float(customer.debt_amount),
            days_since_last_order=days_since_last_order
        )
        
        return CustomerStatusCheck(
            customer_id=customer.id,
            phone=customer.phone,
            full_name=f"{customer.first_name} {customer.last_name}",
            segment=customer.segment,
            status=customer.status,
            is_vip=is_vip,
            is_gold=is_gold,
            has_debt=has_debt,
            is_inactive=is_inactive,
            is_blocked=is_blocked,
            total_orders=customer.total_orders,
            total_spent=float(customer.total_spent),
            debt_amount=float(customer.debt_amount),
            last_order_date=customer.last_order_date,
            days_since_last_order=days_since_last_order,
            recommendation=recommendation
        )
    
    @staticmethod
    def _determine_recommendation(
        is_vip: bool,
        is_gold: bool,
        has_debt: bool,
        is_inactive: bool,
        is_blocked: bool,
        debt_amount: float,
        days_since_last_order: Optional[int]
    ) -> str:
        """
        Complex branching logic for customer recommendation.
        
        Priority order:
        1. Blocked → Cannot proceed
        2. Has debt → Request payment
        3. VIP → Premium service
        4. Gold → Priority service
        5. Inactive → Re-engagement campaign
        6. Regular → Standard service
        """
        if is_blocked:
            return "BLOCKED: Customer is blocked. Contact admin."
        
        if has_debt:
            return f"DEBT: Customer has outstanding debt of ${debt_amount:.2f}. Request payment before proceeding."
        
        if is_vip:
            return "VIP: Provide premium service. Offer exclusive deals and priority support."
        
        if is_gold:
            return "GOLD: Provide priority service. Offer special discounts."
        
        if is_inactive:
            return f"INACTIVE: Customer hasn't ordered in {days_since_last_order} days. Send re-engagement campaign."
        
        return "REGULAR: Provide standard service. Consider upselling opportunities."
    
    @staticmethod
    async def segment_customer(
        db: AsyncSession,
        customer: Customer
    ) -> CustomerSegmentationResult:
        """
        Automatic customer segmentation based on business rules.
        
        Segmentation Rules:
        - VIP: total_spent >= $10,000 OR total_orders >= 50
        - GOLD: total_spent >= $5,000 OR total_orders >= 25
        - SILVER: total_spent >= $1,000 OR total_orders >= 10
        - BRONZE: total_spent >= $500 OR total_orders >= 5
        - REGULAR: Default
        """
        previous_segment = customer.segment
        total_spent = float(customer.total_spent)
        total_orders = customer.total_orders
        
        # Determine new segment
        new_segment = CustomerSegment.REGULAR
        reason = "Default segment"
        
        if total_spent >= 10000 or total_orders >= 50:
            new_segment = CustomerSegment.VIP
            reason = f"High value customer: ${total_spent:.2f} spent, {total_orders} orders"
        elif total_spent >= 5000 or total_orders >= 25:
            new_segment = CustomerSegment.GOLD
            reason = f"Premium customer: ${total_spent:.2f} spent, {total_orders} orders"
        elif total_spent >= 1000 or total_orders >= 10:
            new_segment = CustomerSegment.SILVER
            reason = f"Valued customer: ${total_spent:.2f} spent, {total_orders} orders"
        elif total_spent >= 500 or total_orders >= 5:
            new_segment = CustomerSegment.BRONZE
            reason = f"Regular customer: ${total_spent:.2f} spent, {total_orders} orders"
        
        # Update customer segment if changed
        if new_segment != previous_segment:
            customer.segment = new_segment
            await db.commit()
            await db.refresh(customer)
            
            # Invalidate cache
            cache_key = CustomerService._get_cache_key(customer.tenant_id, customer.phone)
            redis_client = await CustomerService.get_redis_client()
            await redis_client.delete(cache_key)
        
        return CustomerSegmentationResult(
            customer_id=customer.id,
            previous_segment=previous_segment,
            new_segment=new_segment,
            reason=reason,
            metrics={
                "total_spent": total_spent,
                "total_orders": total_orders,
                "lifetime_value": float(customer.lifetime_value)
            }
        )
    
    @staticmethod
    async def create_customer(
        db: AsyncSession,
        tenant_id: UUID,
        customer_data: CustomerCreate
    ) -> Customer:
        """Create a new customer."""
        # Check if customer with phone already exists
        existing, _ = await CustomerService.get_customer_by_phone(
            db, tenant_id, customer_data.phone, use_cache=False
        )
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this phone number already exists"
            )
        
        customer = Customer(
            **customer_data.model_dump(),
            tenant_id=tenant_id
        )
        
        db.add(customer)
        
        try:
            await db.commit()
            await db.refresh(customer)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create customer"
            )
        
        return customer
    
    @staticmethod
    async def update_customer(
        db: AsyncSession,
        tenant_id: UUID,
        customer_id: UUID,
        customer_data: CustomerUpdate
    ) -> Customer:
        """Update customer and invalidate cache."""
        query = select(Customer).where(
            and_(
                Customer.id == customer_id,
                Customer.tenant_id == tenant_id
            )
        )
        
        result = await db.execute(query)
        customer = result.scalar_one_or_none()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Update fields
        update_dict = customer_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(customer, field, value)
        
        await db.commit()
        await db.refresh(customer)
        
        # ⚡ Cache Invalidation: Delete cache immediately on update
        cache_key = CustomerService._get_cache_key(tenant_id, customer.phone)
        redis_client = await CustomerService.get_redis_client()
        deleted = await redis_client.delete(cache_key)
        print(f"🗑️  Cache invalidated for {customer.phone}: {deleted} key(s) deleted")
        
        return customer
    
    @staticmethod
    async def list_customers(
        db: AsyncSession,
        tenant_id: UUID,
        segment: Optional[CustomerSegment] = None,
        status: Optional[CustomerStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Customer]:
        """List customers with filters."""
        query = select(Customer).where(Customer.tenant_id == tenant_id)
        
        if segment:
            query = query.where(Customer.segment == segment)
        
        if status:
            query = query.where(Customer.status == status)
        
        query = query.order_by(Customer.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_customer_stats(
        db: AsyncSession,
        customer_id: UUID,
        order_amount: float
    ) -> Customer:
        """
        Update customer statistics after an order.
        Triggers automatic segmentation.
        """
        query = select(Customer).where(Customer.id == customer_id)
        result = await db.execute(query)
        customer = result.scalar_one_or_none()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Update stats
        customer.total_orders += 1
        customer.total_spent += order_amount
        customer.lifetime_value += order_amount
        customer.last_order_date = datetime.utcnow()
        customer.last_contact_date = datetime.utcnow()
        
        await db.commit()
        await db.refresh(customer)
        
        # Auto-segment customer
        await CustomerService.segment_customer(db, customer)
        
        # ⚡ Cache Invalidation: Delete cache immediately on stats update
        cache_key = CustomerService._get_cache_key(customer.tenant_id, customer.phone)
        redis_client = await CustomerService.get_redis_client()
        deleted = await redis_client.delete(cache_key)
        print(f"🗑️  Cache invalidated for {customer.phone}: {deleted} key(s) deleted")
        
        return customer
