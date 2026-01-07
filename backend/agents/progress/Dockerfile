# Multi-stage Dockerfile for Progress Tracker Agent

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

COPY backend/agents/progress /app/backend/agents/progress

ENV PYTHONPATH=/app
ENV PORT=8006

CMD ["uvicorn", "backend.agents.progress.main:app", "--host", "0.0.0.0", "--port", "8006", "--reload"]

# Production stage
FROM base as production

COPY backend/agents/progress /app/backend/agents/progress

ENV PYTHONPATH=/app
ENV PORT=8006

# Run as non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

CMD ["uvicorn", "backend.agents.progress.main:app", "--host", "0.0.0.0", "--port", "8006", "--workers", "2"]
