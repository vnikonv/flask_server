"""
# This function generates a secret key for the Flask application to sign secure user/client session cookies.
"""
import secrets

def keygen() -> str:
    return secrets.token_hex(64)  # Generates a random secret key of 64 bytes or 128 hex characters
