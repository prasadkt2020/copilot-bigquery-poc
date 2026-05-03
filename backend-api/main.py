# main.py
# main.py
from flask import Flask, jsonify, abort
from google.cloud import bigquery
from auth import validate_token

app = Flask(__name__)

def get_bq():
    return bigquery.Client()

PROJECT = "copilot-bigquery-demo"
DATA_TABLE = f"{PROJECT}.sample_dataset.sample_table"
RLS_TABLE = f"{PROJECT}.security_manual.manual_rls"


@app.route("/orders", methods=["GET"])
def get_orders():
    # 1. Validate JWT
    claims = validate_token()

    # 2. Extract OID
    oid = claims.get("oid")
    if not oid:
        abort(401, "Token missing oid claim")

    # 3. RLS query
    query = f"""
        SELECT id, name, amount, customer_id, securityhash
        FROM `{DATA_TABLE}`
        WHERE securityhash IN (
            SELECT securityhash
            FROM `{RLS_TABLE}`
            WHERE oid = @oid
        )
        ORDER BY id
    """

    job = get_bq().query(
        query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("oid", "STRING", oid)
            ]
        ),
    )

    rows = [dict(row) for row in job]
    return jsonify(rows)
