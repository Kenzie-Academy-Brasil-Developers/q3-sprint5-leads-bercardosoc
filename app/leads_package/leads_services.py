from click import MissingParameter


def validate_keys(payload: dict, expected_keys: set):

    body_keys = set(payload.keys())
    
    invalid_keys = body_keys - expected_keys

    missing_keys = len(body_keys) - len(expected_keys)

    if invalid_keys:
        raise KeyError(
            {
                "error": "invalid_keys",
                "expected": list(expected_keys),
                "wrong_key(s)": list(invalid_keys)
            }
        )

    if missing_keys < 0:
        raise MissingParameter(
            {
                "error": "missing_keys",
                "expected": list(expected_keys),
                "received": list(body_keys)
            }
        )