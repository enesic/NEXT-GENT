from typing import Any, List, Union
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "NextGent"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Encryption for PII (KVKK/GDPR Compliance)
    ENCRYPTION_KEY: str = "fXACJ43AmGdLJSumrunA2mUtLpD12RTqaAMsu5CEzsU="  # Fernet key for encrypting sensitive data
    
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
    POSTGRES_SERVER: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PORT: int = 5432

    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Union[str, None], info) -> Any:
        if isinstance(v, str):
            return v
        if info.data.get("DATABASE_URL"):
            return info.data.get("DATABASE_URL")

        postgres_server = info.data.get("POSTGRES_SERVER")
        postgres_user = info.data.get("POSTGRES_USER")
        postgres_password = info.data.get("POSTGRES_PASSWORD")
        postgres_db = info.data.get("POSTGRES_DB")
        postgres_port = info.data.get("POSTGRES_PORT")
        if not all([postgres_server, postgres_user, postgres_password, postgres_db, postgres_port]):
            return None
        
        # Build async connection string
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=postgres_user,
            password=postgres_password,
            host=postgres_server,
            port=postgres_port,
            path=f"{postgres_db or ''}",
        )

    # Redis (Optional - system works without it, just slower)
    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    
    REDIS_URL: Union[RedisDsn, str, None] = None
    
    # AI Configuration
    OPENAI_API_KEY: str = "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"
    AI_MODEL: str = "gpt-4o-mini"  # Cost-effective default
    AI_ENABLED: bool = True
    
    @field_validator("REDIS_URL", mode="before")
    def assemble_redis_connection(cls, v: Union[str, None], info) -> Any:
        if isinstance(v, str):
            return v
        
        redis_host = info.data.get("REDIS_HOST")
        if not redis_host:
            return None
            
        return RedisDsn.build(
            scheme="redis",
            host=redis_host,
            port=info.data.get("REDIS_PORT"),
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

settings = Settings()
