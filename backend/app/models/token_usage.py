"""
Token Usage Model - AI Token Consumption Tracking
"""
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin


class TokenUsage(Base, UUIDMixin, TimestampMixin):
    """
    Track AI token consumption for billing and analytics.
    Linked to VAPICall for detailed tracking.
    """
    __tablename__ = "token_usage"
    
    # Foreign Keys
    call_id: Mapped[str] = mapped_column(
        String, 
        nullable=True,  # Make nullable to avoid constraint issues
        index=True
    )
    tenant_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
        index=True
    )
    
    # Token Details
    model_name: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "gpt-4", "gpt-3.5-turbo"
    tokens_prompt: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Input tokens
    tokens_completion: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Output tokens
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Sum of both
    
    # Cost Estimation (USD)
    estimated_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Metadata
    call_duration_seconds: Mapped[float] = mapped_column(Float, nullable=True)
    success: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Relationships
    # call = relationship("VAPICall", back_populates="token_usage")
    
    __table_args__ = (
        Index('idx_token_created_at', 'created_at'),
        Index('idx_token_tenant_date', 'tenant_id', 'created_at'),
        Index('idx_token_model', 'model_name', 'created_at'),
    )
    
    def __repr__(self):
        return f"<TokenUsage {self.model_name} - {self.total_tokens} tokens>"
    
    @classmethod
    def calculate_cost(cls, model_name: str, tokens_prompt: int, tokens_completion: int) -> float:
        """
        Calculate estimated cost based on model pricing.
        Prices are per 1K tokens (approximate).
        """
        pricing = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
            "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
            "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
            "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
        }
        
        model_pricing = pricing.get(model_name, {"prompt": 0.001, "completion": 0.002})
        
        prompt_cost = (tokens_prompt / 1000) * model_pricing["prompt"]
        completion_cost = (tokens_completion / 1000) * model_pricing["completion"]
        
        return round(prompt_cost + completion_cost, 6)
    
    @classmethod
    def create_usage(
        cls,
        call_id: str,
        model_name: str,
        tokens_prompt: int,
        tokens_completion: int,
        tenant_id: str = None,
        call_duration_seconds: float = None,
        success: bool = True
    ):
        """Factory method to create token usage with calculated cost"""
        total_tokens = tokens_prompt + tokens_completion
        estimated_cost = cls.calculate_cost(model_name, tokens_prompt, tokens_completion)
        
        return cls(
            call_id=call_id,
            tenant_id=tenant_id,
            model_name=model_name,
            tokens_prompt=tokens_prompt,
            tokens_completion=tokens_completion,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            call_duration_seconds=call_duration_seconds,
            success=success
        )
