from typing import Any, List, Union
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Union[str, None], info) -> Any:
        if isinstance(v, str):
            return v
        
        # Build async connection string
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=info.data.get("POSTGRES_PORT"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    
    REDIS_URL: Union[RedisDsn, str, None] = None
    
    # AI Configuration
    OPENAI_API_KEY: str = "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"
    AI_MODEL: str = "gpt-4o-mini"  # Cost-effective default
    AI_ENABLED: bool = True
    
    @field_validator("REDIS_URL", mode="before")
    def assemble_redis_connection(cls, v: Union[str, None], info) -> Any:
        if isinstance(v, str):
            return v
            
        return RedisDsn.build(
            scheme="redis",
            host=info.data.get("REDIS_HOST"),
            port=info.data.get("REDIS_PORT"),
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

settings = Settings()
