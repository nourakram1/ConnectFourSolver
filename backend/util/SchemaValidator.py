from jsonschema import validate, ValidationError, Draft7Validator

class SchemaValidator:
    SOLVER_SCHEMA = {
        "type": "object",
        "properties": {
            "board": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "integer", "enum": [0, 1, 2]},
                    "minItems": 7,
                    "maxItems": 7
                },
                "minItems": 6,
                "maxItems": 6
            },
            "algorithm": {
                "type": "string",
                "enum": ["minimax", "expectiminimax"]
            },
            "depth": {"type": "integer", "minimum": 1, "default": 4},
            "prune": {"type": "boolean", "default": True},
            "ai_player": {"type": "boolean", "default": True}
        },
        "required": ["board", "algorithm"],
        "additionalProperties": False
    }

    @staticmethod
    def validate(data: dict) -> tuple[bool, str | None, dict]:
        """
        Validate the input and fill defaults if missing.
        Returns: (is_valid, error_message, validated_data_with_defaults)
        """
        properties = SchemaValidator.SOLVER_SCHEMA.get("properties", {})
        validated_data = data.copy()
        for prop, subschema in properties.items():
            if "default" in subschema and prop not in validated_data:
                validated_data[prop] = subschema["default"]

        try:
            validate(instance=validated_data, schema=SchemaValidator.SOLVER_SCHEMA)
        except ValidationError as e:
            return False, e.message, validated_data

        return True, None, validated_data
