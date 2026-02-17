from typing import Dict, Any, List

class KVKKMasker:
    """
    Handles privacy masking for sensitive data based on tenant configuration.
    """
    
    MASK_CHAR = "*"
    
    @staticmethod
    def mask_data(data: Dict[str, Any], sensitive_keys: List[str]) -> Dict[str, Any]:
        """
        Masks the values of keys specified in sensitive_keys.
        Example: { "patient_id": "12345678901" } -> { "patient_id": "12*******01" }
        """
        if not data or not sensitive_keys:
            return data
            
        masked_data = data.copy()
        
        for key in sensitive_keys:
            if key in masked_data and masked_data[key]:
                val = str(masked_data[key])
                if len(val) > 4:
                    # Keep first 2 and last 2 chars visible
                    masked_val = val[:2] + (KVKKMasker.MASK_CHAR * (len(val) - 4)) + val[-2:]
                    masked_data[key] = masked_val
                else:
                    # Mask completely if too short
                    masked_data[key] = KVKKMasker.MASK_CHAR * len(val)
                    
        return masked_data

    @staticmethod
    def get_privacy_rules(sector: str) -> List[str]:
        """
        Returns default sensitive keys for known sectors.
        """
        defaults = {
            "medical": ["patient_id", "policy_no", "diagnosis"],
            "legal": ["case_no", "client_identity", "settlement_amount"],
            "real_estate": ["budget_range", "client_identity"]
        }
        return defaults.get(sector, [])
