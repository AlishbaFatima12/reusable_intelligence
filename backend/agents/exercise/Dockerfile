# Exercise Generator Agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy shared code and agent code
COPY backend/shared /app/backend/shared
COPY backend/agents/exercise /app/backend/agents/exercise

# Install dependencies
RUN pip install --no-cache-dir -r backend/agents/exercise/requirements.txt

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV AGENT_PORT=8005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8005/health')"

# Expose port
EXPOSE 8005

# Run the agent
CMD ["python", "-m", "backend.agents.exercise.main"]
