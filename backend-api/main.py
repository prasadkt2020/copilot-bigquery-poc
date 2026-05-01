from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)

client = bigquery.Client.from_service_account_json(
    "service-account.json",
    project="copilot-bigquery-demo"
)

@app.post("/query")
def run_query():
    try:
        sql = request.json.get("sql")
        query_job = client.query(sql)
        rows = [dict(row) for row in query_job]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
