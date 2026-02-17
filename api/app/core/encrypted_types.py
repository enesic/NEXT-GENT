"""
Custom SQLAlchemy types for encrypted fields.
Provides transparent encryption/decryption for PII data.
"""
from typing import Any, Optional
from sqlalchemy import String, Text, TypeDecorator
from app.core.encryption import encryption_service


class EncryptedString(TypeDecorator):
    """
    SQLAlchemy type for encrypted string fields.
    Automatically encrypts on write and decrypts on read.
    """
    impl = String
    cache_ok = True

    def __init__(self, length: int = 255, *args, **kwargs):
        # Encrypted data is longer than plaintext (base64 encoding)
        # Allocate extra space for encryption overhead
        super().__init__(length * 2, *args, **kwargs)

    def process_bind_param(self, value: Optional[str], dialect) -> Optional[str]:
        """Encrypt value before storing in database"""
        if value is not None:
            return encryption_service.encrypt_pii(value)
        return value

    def process_result_value(self, value: Optional[str], dialect) -> Optional[str]:
        """Decrypt value when reading from database"""
        if value is not None:
            try:
                return encryption_service.decrypt_pii(value)
            except Exception as e:
                # If decryption fails, might be unencrypted legacy data
                # Return as-is for backward compatibility during migration
                return value
        return value


class EncryptedText(TypeDecorator):
    """
    SQLAlchemy type for encrypted text fields (larger content).
    Automatically encrypts on write and decrypts on read.
    """
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Optional[str], dialect) -> Optional[str]:
        """Encrypt value before storing in database"""
        if value is not None:
            return encryption_service.encrypt_pii(value)
        return value

    def process_result_value(self, value: Optional[str], dialect) -> Optional[str]:
        """Decrypt value when reading from database"""
        if value is not None:
            try:
                return encryption_service.decrypt_pii(value)
            except Exception as e:
                # If decryption fails, might be unencrypted legacy data
                # Return as-is for backward compatibility during migration
                return value
        return value
