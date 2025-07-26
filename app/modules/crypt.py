import secrets

def keygen() -> str:
    """
    # This function generates a secret key for the Flask application to sign secure user/client cookies.
    """
    return secrets.token_hex(64)  # Generates a random secret key of 64 bytes or 128 hex characters
