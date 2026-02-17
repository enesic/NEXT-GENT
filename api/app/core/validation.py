from typing import Dict, Any, List, Optional
from pydantic import ValidationError, create_model

class ContextValidator:
    """
    Validates dynamic data against tenant-specific rules stored in configuration.
    Example Rule Config:
    {
        "patient_id": { "type": "str", "required": true, "pattern": "^[0-9]{11}$" },
        "policy_no": { "type": "str", "required": false }
    }
    """
    
    @staticmethod
    def validate_metadata(metadata: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates metadata against the provided ruleset.
        Raises ValidationError if validation fails.
        """
        if not rules:
            return metadata

        # Dynamic Pydantic model creation
        field_definitions = {}
        for field_name, rule in rules.items():
            field_type = str
            if rule.get('type') == 'int':
                field_type = int
            elif rule.get('type') == 'float':
                field_type = float
            elif rule.get('type') == 'bool':
                field_type = bool
            elif rule.get('type') == 'list':
                field_type = List[Any]

            # Use Optional if not required
            if not rule.get('required', False):
                field_definitions[field_name] = (Optional[field_type], None)
            else:
                field_definitions[field_name] = (field_type, ...)

        # Create model and validate
        DynamicModel = create_model('DynamicMetadataValidator', **field_definitions)
        
        try:
            validated_data = DynamicModel(**metadata)
            return validated_data.model_dump(exclude_unset=True)
        except ValidationError as e:
            # Re-raise with clearer context if needed
            raise ValueError(f"Metadata validation failed: {str(e)}")

    @staticmethod
    def get_sector_rules(sector: str) -> Dict[str, Any]:
        """
        Returns default validation rules for known sectors.
        """
        defaults = {
            "medical": {
                "patient_id": {"type": "str", "required": True},
                "policy_no": {"type": "str", "required": False},
                "doctor_notes": {"type": "str", "required": False}
            },
            "legal": {
                "case_no": {"type": "str", "required": True},
                "court": {"type": "str", "required": True},
                "judge_name": {"type": "str", "required": False}
            },
            "real_estate": {
                "property_id": {"type": "str", "required": True},
                "budget_range": {"type": "str", "required": False},
                "preferred_location": {"type": "str", "required": False}
            }
        }
        return defaults.get(sector, {})
