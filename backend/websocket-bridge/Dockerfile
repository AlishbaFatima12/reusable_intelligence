# Dockerfile for WebSocket Bridge Service

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/websocket-bridge/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/websocket-bridge /app/

ENV PYTHONPATH=/app
ENV SOCKETIO_PORT=4001

# Run as non-root user
RUN useradd -m -u 1000 bridge && chown -R bridge:bridge /app
USER bridge

CMD ["python", "main.py"]
