FROM python:3.13-alpine

WORKDIR /app

# Install dependencies first — this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application code
COPY app/ ./app/

# Run as non-root for security
RUN adduser -D appuser
USER appuser

EXPOSE 8080

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app.app:app"]
