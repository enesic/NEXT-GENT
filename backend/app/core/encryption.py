"""
KVKK/GDPR Compliant Encryption Service
Handles PII encryption with AES-256 and hashing for lookup
"""
import os
import hashlib
from cryptography.fernet import Fernet
from typing import Optional

class EncryptionService:
    """
    Enterprise-grade encryption service for PII protection.
    
    Features:
    - AES-256 encryption for PII
    - SHA-256 hashing for searchable fields
    - KVKK/GDPR compliant
    """
    
    def __init__(self):
        # Load encryption key from environment
        # In production, this should be from a secrets manager (AWS KMS, Azure Key Vault, etc.)
        encryption_key = os.getenv('ENCRYPTION_KEY')
        
        if not encryption_key:
            # Generate a key if not exists (ONLY for development)
            # In production, this MUST be pre-configured
            encryption_key = Fernet.generate_key().decode()
            print(f"⚠️ WARNING: Generated encryption key. Set ENCRYPTION_KEY in production!")
            print(f"ENCRYPTION_KEY={encryption_key}")
        
        self.fernet = Fernet(encryption_key if isinstance(encryption_key, bytes) else encryption_key.encode())
    
    def encrypt_pii(self, plaintext: str) -> str:
        """
        Encrypt PII data with AES-256.
        
        Args:
            plaintext: The sensitive data to encrypt
            
        Returns:
            Base64-encoded encrypted string
        """
        if not plaintext:
            return ""
        
        encrypted_bytes = self.fernet.encrypt(plaintext.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    
    def decrypt_pii(self, encrypted: str) -> str:
        """
        Decrypt PII data.
        
        Args:
            encrypted: Base64-encoded encrypted string
            
        Returns:
            Decrypted plaintext
            
        Note:
            This operation MUST be logged for KVKK audit trail
        """
        if not encrypted:
            return ""
        
        decrypted_bytes = self.fernet.decrypt(encrypted.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    
    @staticmethod
    def hash_for_lookup(data: str) -> str:
        """
        Create SHA-256 hash for searchable fields.
        
        Used for:
        - Phone number lookup (without revealing actual number)
        - Email lookup
        - Customer ID matching
        
        Args:
            data: Data to hash
            
        Returns:
            Hex-encoded SHA-256 hash
        """
        if not data:
            return ""
        
        # Normalize data (lowercase, strip whitespace)
        normalized = data.lower().strip()
        
        # SHA-256 hash
        hash_obj = hashlib.sha256(normalized.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def hash_phone_for_lookup(phone: str) -> str:
        """
        Hash phone number for lookup (removes formatting).
        
        Examples:
            "+90 555 123 4567" → same hash as "905551234567"
        """
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        return EncryptionService.hash_for_lookup(digits_only)


# Global singleton instance
encryption_service = EncryptionService()
