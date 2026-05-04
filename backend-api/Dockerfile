FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth.py .
COPY main.py .

CMD ["gunicorn", "--workers", "1", "--timeout", "180", "--bind", "0.0.0.0:8080", "main:app"]
