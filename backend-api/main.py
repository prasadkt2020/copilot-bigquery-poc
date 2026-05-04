from flask import Flask, jsonify, request
from auth import validate_jwt, AuthError
from google.cloud import bigquery

app = Flask(__name__)

# BigQuery client
bq_client = bigquery.Client()


@app.route("/list", methods=["GET"])
def list_sales():
    auth_header = request.headers.get("Authorization", "")

    try:
        claims = validate_jwt(auth_header)
    except AuthError as e:
        return jsonify({"error": str(e)}), 401

    oid = claims.get("oid") or claims.get("sub")
    if not oid:
        return jsonify({"error": "No OID found in token"}), 401

    query = f"""
        SELECT s.*
        FROM `sales_data.sales` s
        JOIN `sales_data.user_access` u
        ON s.region = u.region
        WHERE u.oid = '{oid}'
    """

    query_job = bq_client.query(query)
    rows = [dict(row) for row in query_job]

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
