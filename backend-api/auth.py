# backend-api/auth.py
import os
import time
import requests
import jwt
from jwt import PyJWKClient
from typing import Dict, Any

TENANT_ID = os.getenv("TENANT_ID", "810d0f9b-27ba-42c7-9718-f32165fc074b")
API_APP_ID = os.getenv("API_APP_ID", "732af741-d74a-44ce-bd01-1e6a76040b17")

ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL = f"{ISSUER}/discovery/v2.0/keys"
AUDIENCE = f"api://{API_APP_ID}"

_jwks_client = PyJWKClient(JWKS_URL)


class AuthError(Exception):
    pass


def _get_bearer_token(auth_header: str) -> str:
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise AuthError("Missing or invalid Authorization header")
    return auth_header.split(" ", 1)[1].strip()


def validate_jwt(auth_header: str) -> Dict[str, Any]:
    """
    Validates an Entra ID JWT:
    - Extracts Bearer token
    - Fetches signing key from JWKS
    - Validates signature, issuer, audience, expiry
    Returns decoded claims if valid, raises AuthError otherwise.
    """
    token = _get_bearer_token(auth_header)

    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token).key

        claims = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
        )

        now = int(time.time())
        if claims.get("exp") and now > claims["exp"]:
            raise AuthError("Token expired")

        return claims

    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired")
    except jwt.InvalidTokenError as e:
        raise AuthError(f"Invalid token: {str(e)}")
