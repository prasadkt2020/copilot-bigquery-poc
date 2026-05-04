from flask import Flask, jsonify, request
from auth import validate_jwt, AuthError
from google.cloud import bigquery

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
        return jsonify({"error": "No OID found in token"}), 401

    query = """
        SELECT
          f.id,
          f.name,
          f.amount,
          f.created_at,
          f.customer_id,
          f.securityhash
        FROM `copilot-bigquery-demo.sample_dataset.sample_table` AS f
        INNER JOIN `copilot-bigquery-demo.security_manual.manual_rls` AS r
          ON f.securityhash = r.securityhash
        WHERE r.oid = @oid
        ORDER BY f.created_at DESC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("oid", "STRING", oid),
        ]
    )

    query_job = bq_client.query(query, job_config=job_config)

    rows = [dict(row) for row in query_job]

    return jsonify({"oid": oid, "rows": rows})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
