import requests
from jose import jwt
from flask import request, abort

TENANT_ID = "810d0f9b-27ba-42c7-9718-f32165fc074b"
AUDIENCE = "api://8fbdfb12-b319-442a-b894-bf837f18dee5"
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"

JWKS_URL = f"{ISSUER}/discovery/v2.0/keys"
JWKS = requests.get(JWKS_URL).json()

def validate_token():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        abort(401, "Missing Authorization header")

    if not auth_header.startswith("Bearer "):
        abort(401, "Invalid Authorization header format")

    token = auth_header.replace("Bearer ", "")

    try:
        unverified_header = jwt.get_unverified_header(token)

        key = next(
            k for k in JWKS["keys"]
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