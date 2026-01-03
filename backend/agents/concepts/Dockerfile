# Multi-stage Dockerfile for Concepts Agent

FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy shared dependencies
COPY backend/shared /app/backend/shared
COPY backend/requirements.txt /app/backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Development stage
FROM base as development

COPY backend/agents/concepts /app/backend/agents/concepts

ENV PYTHONPATH=/app
ENV PORT=8002

CMD ["uvicorn", "backend.agents.concepts.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]

# Production stage
FROM base as production

COPY backend/agents/concepts /app/backend/agents/concepts

ENV PYTHONPATH=/app
ENV PORT=8002

# Run as non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

CMD ["uvicorn", "backend.agents.concepts.main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "2"]
