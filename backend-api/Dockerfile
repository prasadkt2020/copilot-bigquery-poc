# Use the official lightweight Python image.
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 for Cloud Run
ENV PORT=8080

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
