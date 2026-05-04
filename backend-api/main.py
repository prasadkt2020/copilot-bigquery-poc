# backend-api/main.py
from flask import Flask, request, jsonify
from google.cloud import bigquery
from auth import validate_jwt, AuthError

app = Flask(__name__)
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
        return jsonify({"error": "Missing oid in token"}), 403

    query = """
    SELECT s.*
    FROM `copilot-bigquery-demo.sample_dataset.sample_table` s
    JOIN `copilot-bigquery-demo.security_manual.manual_rls` r
      ON s.securityhash = r.securityhash
    WHERE r.oid = @oid
    """

    job = bq_client.query(
        query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("oid", "STRING", oid)
            ]
        ),
    )

    rows = [dict(row) for row in job.result()]
    return jsonify(rows), 200


@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200


# ⭐ THIS WAS THE MISSING PIECE ⭐
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
