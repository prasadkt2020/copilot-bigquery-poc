# auth.py
import os
from jose import jwt
import requests

TENANT_ID = os.getenv("TENANT_ID")
AUDIENCE = os.getenv("AUDIENCE")

DISCOVERY_URL = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"

_discovery_cache = None
_jwks_cache = None


def get_discovery():
    global _discovery_cache
    if _discovery_cache is None:
        resp = requests.get(DISCOVERY_URL, timeout=5)
        resp.raise_for_status()
        _discovery_cache = resp.json()
    return _discovery_cache


def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
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


def verify_jwt_and_get_email(token):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    public_key = get_public_key(kid)
    if not public_key:
        raise Exception("Unable to find matching JWKS key")

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
    )

    return decoded.get("preferred_username") or decoded.get("email")
