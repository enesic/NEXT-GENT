import re
from typing import Any, Dict, Optional
import hashlib


class PIIMasker:
    """
    Personal Identifiable Information (PII) masker for KVKK/GDPR compliance.
    
    Masks sensitive data in logs:
    - Phone numbers
    - Email addresses
    - Names
    - Credit card numbers
    - National IDs
    """
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        Mask phone number for logging.
        
        Examples:
        +905551234567 → +9055512****7
        05551234567 → 055512****7
        """
        if not phone or len(phone) < 4:
            return "****"
        
        # Remove non-digit characters for processing
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) < 4:
            return "****"
        
        # Keep first 6 and last 1 digit, mask the rest
        if len(digits) > 7:
            masked = digits[:6] + "*" * (len(digits) - 7) + digits[-1:]
        else:
            masked = digits[:2] + "*" * (len(digits) - 2)
        
        # Preserve original format (with + if present)
        if phone.startswith('+'):
            return '+' + masked
        return masked
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email address for logging.
        
        Examples:
        ahmet.yilmaz@example.com → ah***@example.com
        test@gmail.com → te***@gmail.com
        """
        if not email or '@' not in email:
            return "****@****.com"
        
        local, domain = email.split('@', 1)
        
        if len(local) <= 2:
            masked_local = local[0] + "***"
        else:
            masked_local = local[:2] + "***"
        
        return f"{masked_local}@{domain}"
    
    @staticmethod
    def mask_name(name: str) -> str:
        """
        Mask person name for logging.
        
        Examples:
        Ahmet Yılmaz → A*** Y***
        John Doe Smith → J*** D*** S***
        """
        if not name:
            return "****"
        
        words = name.split()
        masked_words = []
        
        for word in words:
            if len(word) <= 1:
                masked_words.append(word)
            else:
                masked_words.append(word[0] + "***")
        
        return " ".join(masked_words)
    
    @staticmethod
    def mask_credit_card(card: str) -> str:
        """
        Mask credit card number.
        
        Examples:
        1234567890123456 → 1234********3456
        """
        digits = re.sub(r'\D', '', card)
        
        if len(digits) < 8:
            return "****"
        
        return digits[:4] + "*" * (len(digits) - 8) + digits[-4:]
    
    @staticmethod
    def hash_pii(data: str) -> str:
        """
        Create one-way hash of PII for tracking without exposing data.
        
        Useful for:
        - Tracking unique users without storing phone/email
        - Correlation in logs without exposing PII
        
        Example:
        +905551234567 → a3f2b1c...
        """
        return hashlib.sha256(data.encode()).hexdigest()[:12]
    
    @staticmethod
    def mask_dict(data: Dict[str, Any], sensitive_keys: Optional[list] = None) -> Dict[str, Any]:
        """
        Recursively mask sensitive fields in dictionary.
        
        Args:
            data: Dictionary to mask
            sensitive_keys: List of keys to mask (default: common PII fields)
        
        Returns:
            Masked dictionary
        """
        if sensitive_keys is None:
            sensitive_keys = [
                'phone', 'phone_number', 'customer_number', 'mobile',
                'email', 'email_address',
                'name', 'first_name', 'last_name', 'full_name', 'client_name',
                'credit_card', 'card_number',
                'ssn', 'national_id', 'tc_no'
            ]
        
        masked_data = {}
        
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursive masking for nested dicts
                masked_data[key] = PIIMasker.mask_dict(value, sensitive_keys)
            elif isinstance(value, list):
                # Mask list items
                masked_data[key] = [
                    PIIMasker.mask_dict(item, sensitive_keys) if isinstance(item, dict) else item
                    for item in value
                ]
            elif key.lower() in [k.lower() for k in sensitive_keys]:
                # Mask sensitive field
                if 'phone' in key.lower() or 'mobile' in key.lower():
                    masked_data[key] = PIIMasker.mask_phone(str(value))
                elif 'email' in key.lower():
                    masked_data[key] = PIIMasker.mask_email(str(value))
                elif 'name' in key.lower():
                    masked_data[key] = PIIMasker.mask_name(str(value))
                elif 'card' in key.lower():
                    masked_data[key] = PIIMasker.mask_credit_card(str(value))
                else:
                    masked_data[key] = "***MASKED***"
            else:
                masked_data[key] = value
        
        return masked_data
    
    @staticmethod
    def safe_log(message: str, **kwargs) -> str:
        """
        Create safe log message with masked PII.
        
        Usage:
        safe_log("Processing customer", phone="+905551234567", email="test@example.com")
        → "Processing customer | phone=+9055512****7 | email=te***@example.com"
        """
        masked_parts = [message]
        
        for key, value in kwargs.items():
            if 'phone' in key.lower():
                masked_value = PIIMasker.mask_phone(str(value))
            elif 'email' in key.lower():
                masked_value = PIIMasker.mask_email(str(value))
            elif 'name' in key.lower():
                masked_value = PIIMasker.mask_name(str(value))
            else:
                masked_value = value
            
            masked_parts.append(f"{key}={masked_value}")
        
        return " | ".join(masked_parts)


# Singleton instance
pii_masker = PIIMasker()
