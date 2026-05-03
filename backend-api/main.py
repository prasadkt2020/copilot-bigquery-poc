# main.py
import os
from flask import Flask, request, abort, jsonify
from auth import validate_token

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")  # simple shared secret for PoC


def check_api_key():
    expected = API_KEY
    if not expected:
        return  # disabled if not set
    provided = request.headers.get("x-api-key")
    if provided != expected:
        abort(401, "Invalid API key")


@app.route("/orders", methods=["GET"])
def get_orders():
    check_api_key()
    claims = validate_token()
    oid = claims.get("oid")
    # ... your existing BigQuery + RLS logic ...
    return jsonify([])  # placeholder
