"""
Tests for PII Masker - KVKK/GDPR Compliance
"""
import pytest
from app.core.pii_masker import PIIMasker


class TestPIIMasker:
    """Test PII masking functionality."""
    
    def test_mask_phone_turkish(self):
        """Test Turkish phone number masking."""
        masker = PIIMasker()
        
        # Turkish mobile
        assert masker.mask_phone("+905551234567") == "+9055512****7"
        assert masker.mask_phone("05551234567") == "055512****7"
        
        # Short number
        assert masker.mask_phone("123") == "****"
    
    def test_mask_email(self):
        """Test email masking."""
        masker = PIIMasker()
        
        assert masker.mask_email("ahmet.yilmaz@example.com") == "ah***@example.com"
        assert masker.mask_email("test@gmail.com") == "te***@gmail.com"
        assert masker.mask_email("a@b.com") == "a***@b.com"
    
    def test_mask_name(self):
        """Test name masking."""
        masker = PIIMasker()
        
        assert masker.mask_name("Ahmet Yılmaz") == "A*** Y***"
        assert masker.mask_name("John Doe Smith") == "J*** D*** S***"
        assert masker.mask_name("Ali") == "A***"
    
    def test_mask_credit_card(self):
        """Test credit card masking."""
        masker = PIIMasker()
        
        assert masker.mask_credit_card("1234567890123456") == "1234********3456"
        assert masker.mask_credit_card("1234-5678-9012-3456") == "1234********3456"
    
    def test_hash_pii(self):
        """Test PII hashing for tracking."""
        masker = PIIMasker()
        
        # Same input should produce same hash
        hash1 = masker.hash_pii("+905551234567")
        hash2 = masker.hash_pii("+905551234567")
        assert hash1 == hash2
        
        # Different input should produce different hash
        hash3 = masker.hash_pii("+905559876543")
        assert hash1 != hash3
        
        # Hash should be 12 characters
        assert len(hash1) == 12
    
    def test_mask_dict(self):
        """Test dictionary masking."""
        masker = PIIMasker()
        
        data = {
            "phone": "+905551234567",
            "email": "test@example.com",
            "name": "Ahmet Yılmaz",
            "other": "not sensitive"
        }
        
        masked = masker.mask_dict(data)
        
        assert masked["phone"] == "+9055512****7"
        assert masked["email"] == "te***@example.com"
        assert masked["name"] == "A*** Y***"
        assert masked["other"] == "not sensitive"
    
    def test_mask_nested_dict(self):
        """Test nested dictionary masking."""
        masker = PIIMasker()
        
        data = {
            "customer": {
                "phone": "+905551234567",
                "email": "test@example.com"
            },
            "order_id": "12345"
        }
        
        masked = masker.mask_dict(data)
        
        assert masked["customer"]["phone"] == "+9055512****7"
        assert masked["customer"]["email"] == "te***@example.com"
        assert masked["order_id"] == "12345"
    
    def test_safe_log(self):
        """Test safe log message creation."""
        masker = PIIMasker()
        
        log_msg = masker.safe_log(
            "Customer created",
            phone="+905551234567",
            email="test@example.com",
            name="Ahmet Yılmaz"
        )
        
        # Should contain masked values
        assert "+9055512****7" in log_msg
        assert "te***@example.com" in log_msg
        assert "A*** Y***" in log_msg
        
        # Should NOT contain original values
        assert "+905551234567" not in log_msg
        assert "test@example.com" not in log_msg
        assert "Ahmet Yılmaz" not in log_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
