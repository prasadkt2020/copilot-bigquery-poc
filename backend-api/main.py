import os
from flask import Flask, jsonify
from google.cloud import bigquery
from auth import validate_token   # <-- ADD THIS

app = Flask(__name__)

# Initialize BigQuery client once (best practice for Cloud Run)
bq = bigquery.Client()

@app.route("/")
def root():
    return jsonify({
        "status": "ok",
        "message": "Cloud Run API is running"
    })


@app.route("/test")
def test_bigquery():
    validate_token()  # <-- ADD THIS

    query = "SELECT 1 AS test"
    rows = bq.query(query).result()
    result = [dict(row) for row in rows]

    return jsonify({"result": result})


@app.route("/list")
def list_rows():
    validate_token()  # <-- ADD THIS

    query = """
        SELECT *
        FROM `copilot-bigquery-demo.sample_dataset.sample_table`
        LIMIT 10
    """

    rows = bq.query(query).result()
    result = [dict(row) for row in rows]

    return jsonify({
        "status": "ok",
        "row_count": len(result),
        "rows": result
    })


# Cloud Run entrypoint
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
