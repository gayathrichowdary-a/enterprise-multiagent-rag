# auth/auth_utils.py
import hashlib
import os

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False


def hash_password(password: str) -> str:
    """Safely hash passwords using bcrypt if available, else SHA-256."""
    if HAS_BCRYPT:
        try:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        except Exception:
            pass
    # Built-in Python fallback (never crashes)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against stored hash."""
    if HAS_BCRYPT:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            pass
    # Built-in Python fallback check
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == hashed


# Alias so check_password also works anywhere
check_password = verify_password