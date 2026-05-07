# =========================
# Dependencies
# =========================

from typing import Optional
import base64
import binascii
import hashlib
import hmac
import json
import os
import time

# =========================
# Environments
# =========================

SESSION_COOKIE = 'app_session'
SESSION_MAX_AGE = int(os.environ.get('SESSION_MAX_AGE', '3600'))
REMEMBER_SESSION_MAX_AGE = int(os.environ.get('REMEMBER_SESSION_MAX_AGE', '2592000'))
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
SESSION_SECRET = os.environ.get('SESSION_SECRET')

# =========================
# Methods
# =========================

def _b64encode(data: bytes) -> str:
    """
    Encode bytes to a URL-safe base64 string without padding.
    """

    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def _b64decode(data: str) -> bytes:
    """
    Decode a URL-safe base64 string, adding padding if necessary.
    """

    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(f'{data}{padding}')

def _sign(value: str) -> str:
    """
    Sign a value using HMAC with the session secret and returns a URL-safe base64 string.
    """

    digest = hmac.new(
        SESSION_SECRET.encode('utf-8'),
        value.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return _b64encode(digest)

def create_session(email: str, max_age: int = SESSION_MAX_AGE) -> str:
    """
    Create a session token for the given email with an expiration time.
    """

    payload = {
        'email': email,
        'exp': int(time.time()) + max_age
    }
    encoded_payload = _b64encode(
        json.dumps(payload, separators=(',', ':')).encode('utf-8')
    )
    return f'{encoded_payload}.{_sign(encoded_payload)}'


def verify_session(token: Optional[str]) -> Optional[dict]:
    """
    Verify a session token and returns the payload if valid, or None if invalid or expired.
    """

    if not token or '.' not in token:
        return None

    encoded_payload, signature = token.rsplit('.', 1)
    if not hmac.compare_digest(signature, _sign(encoded_payload)):
        return None

    try:
        payload = json.loads(_b64decode(encoded_payload))
    except (binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
        return None

    if int(payload.get('exp', 0)) < int(time.time()):
        return None

    return payload

def check_password(password: str, stored_password: str) -> bool:
    """
    Check if the provided password matches the stored password, which can be either a plain text or a PBKDF2 hash.
    """

    if not password or not stored_password:
        return False

    if not stored_password.startswith('pbkdf2_sha256$'):
        return hmac.compare_digest(password, stored_password)

    try:
        _, iterations, salt, expected_hash = stored_password.split('$', 3)
        calculated_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            bytes.fromhex(salt),
            int(iterations)
        ).hex()
    except (ValueError, TypeError):
        return False

    return hmac.compare_digest(calculated_hash, expected_hash)
