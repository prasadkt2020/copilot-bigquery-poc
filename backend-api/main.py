from flask import Flask, request, jsonify
from google.cloud import bigquery
from auth import verify_jwt_and_get_email

# Lazy global client (created only on first request)
bq_client = None

def get_bq_client():
    global bq_client
    if bq_client is None:
        bq_client = bigquery.Client()
    return bq_client


def create_app():
    app = Flask(__name__)

    # ----------------------------------------------------------------------
    # Health check endpoint (fast, no dependencies)
    # ----------------------------------------------------------------------
    @app.route("/healthz")
    def healthz():
        return "ok", 200

    # ----------------------------------------------------------------------
    # Orders endpoint
    # ----------------------------------------------------------------------
    @app.route("/orders", methods=["GET"])
    def get_orders():
        # Extract JWT from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1]

        # Validate JWT and extract email
        try:
            user_email = verify_jwt_and_get_email(token)
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        # Build BigQuery query with RLS
        query = f"""
            SELECT *
            FROM `copilot-bigquery-demo.sales.orders`
            WHERE customer_email = @user_email
            LIMIT 100
        """

        client = get_bq_client()

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_email", "STRING", user_email)
            ]
        )

        # Execute query
        query_job = client.query(query, job_config=job_config)
        rows = [dict(row) for row in query_job]

        return jsonify({"email": user_email, "orders": rows}), 200

    return app


# Gunicorn entrypoint
app = create_app()
