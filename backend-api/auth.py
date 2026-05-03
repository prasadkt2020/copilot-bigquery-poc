import requests
from jose import jwt
from flask import request, abort

TENANT_ID = "810d0f9b-27ba-42c7-9718-f32165fc074b"

# Accept v1.0 tokens (your tenant issues only these)
ISSUER = f"https://sts.windows.net/{TENANT_ID}/"

# Your API App Registration audience
AUDIENCE = "api://c20b71e8-4c6f-4da7-87d6-af25118c25b6"

# JWKS endpoint for v1.0 tokens
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/keys"

_cached_jwks = None

def get_jwks():
    global _cached_jwks
    if _cached_jwks is None:
        resp = requests.get(JWKS_URL, timeout=5)
        resp.raise_for_status()
        _cached_jwks = resp.json()
    return _cached_jwks


def validate_token():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        abort(401, "Missing Authorization header")

    if not auth_header.startswith("Bearer "):
        abort(401, "Invalid Authorization header format")

    token = auth_header.replace("Bearer ", "")

    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)

        key = next(
            k for k in jwks["keys"]
            if k["kid"] == unverified_header["kid"]
        )

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER
        )

        return payload

    except Exception as e:
        abort(401, f"Invalid token: {str(e)}")
