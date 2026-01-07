# Debug Agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy shared code and agent code
COPY backend/shared /app/backend/shared
COPY backend/agents/debug /app/backend/agents/debug

# Install dependencies
RUN pip install --no-cache-dir -r backend/agents/debug/requirements.txt

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV AGENT_PORT=8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8004/health')"

# Expose port
EXPOSE 8004

# Run the agent
CMD ["python", "-m", "backend.agents.debug.main"]
