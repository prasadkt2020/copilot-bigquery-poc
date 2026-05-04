import jwt
from jwt import PyJWKClient
from flask import request

TENANT_ID = "810d0f9b-27ba-42c7-9718-f32165fc074b"

# Correct JWKS URL for Microsoft Entra ID
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

_jwks_client = PyJWKClient(JWKS_URL)


class AuthError(Exception):
    pass


def _get_bearer_token(auth_header: str) -> str:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthError("Missing or invalid Authorization header")
    return auth_header.split(" ", 1)[1]


def validate_jwt(auth_header: str) -> dict:
    token = _get_bearer_token(auth_header)

    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token).key

        claims = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience="732af741-d74a-44ce-bd01-1e6a76040b17",  # Your API App ID
            options={"verify_exp": True},
        )
        return claims

    except Exception as e:
        raise AuthError(f"JWT validation failed: {str(e)}")
