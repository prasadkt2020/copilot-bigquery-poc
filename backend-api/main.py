import os
from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"status": "ok", "message": "Cloud Run API is running"})


@app.route("/test")
def test_bigquery():
    """
    Simple BigQuery test endpoint.
    Confirms Cloud Run → BigQuery connectivity using service account.
    """
    client = bigquery.Client()

    query = "SELECT 1 AS test"
    rows = client.query(query).result()

    result = [dict(row) for row in rows]
    return jsonify({"result": result})


# Cloud Run entrypoint
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
