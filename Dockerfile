# Build stage (optional: use if you need build deps)
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser wsgi.py .
# Pasta migrations (gere com: flask --app wsgi.py db init && flask --app wsgi.py db migrate -m initial)
COPY --chown=appuser:appuser migrations/ ./migrations/

USER appuser

# Fly.io injects PORT (default 8080)
ENV PORT=8080
EXPOSE 8080

# Gunicorn: bind to all interfaces so Fly can reach the app (shell form to expand $PORT)
CMD ["/bin/sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 2 --timeout 120 wsgi:app"]
