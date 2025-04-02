import hashlib

def encrypt_password_sha256(password: str) -> str:
    """
    Encrypt the given password using SHA-256.

    Args:
        password (str): The password to encrypt.

    Returns:
        str: The SHA-256 encrypted password.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    return sha256_hash.hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify the password against the hashed password.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return encrypt_password_sha256(password) == hashed_password