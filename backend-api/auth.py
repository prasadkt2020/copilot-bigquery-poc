# auth.py
import os
from jose import jwt
import requests
from flask import request, abort


TENANT_ID = os.getenv("TENANT_ID")
AUDIENCE = os.getenv("AUDIENCE")

DISCOVERY_URL = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"

_discovery_cache = None
_jwks_cache = None


def get_discovery():
    global _discovery_cache
    if _discovery_cache:
        return _discovery_cache
    resp = requests.get(DISCOVERY_URL, timeout=5)
    resp.raise_for_status()
    _discovery_cache = resp.json()
    return _discovery_cache


def get_jwks():
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache
    jwks_uri = get_discovery()["jwks_uri"]
    resp = requests.get(jwks_uri, timeout=5)
    resp.raise_for_status()
    _jwks_cache = resp.json()
    return _jwks_cache


def get_public_key(kid):
    jwks = get_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    return None


def validate_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        abort(401, "Invalid token header")

    public_key = get_public_key(unverified_header.get("kid"))
    if not public_key:
        abort(401, "Unable to find matching JWKS key")

    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
        )
        return decoded
    except Exception as e:
        print("Token validation error:", e)
        abort(401, "Invalid token")
