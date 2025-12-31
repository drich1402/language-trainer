# Multi-stage Dockerfile for full-stack deployment on fly.io
# This builds both frontend and backend in a single container

# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with frontend static files
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend files
COPY --from=frontend-builder /frontend/dist /app/static

# Create directory for SQLite database
RUN mkdir -p /data

# Create a startup script that serves both frontend and backend
RUN echo '#!/bin/sh\n\
    import uvicorn\n\
    import os\n\
    \n\
    if __name__ == "__main__":\n\
    port = int(os.getenv("PORT", 8000))\n\
    uvicorn.run("main:app", host="0.0.0.0", port=port)\n\
    ' > start.py

# Expose port (fly.io sets PORT env variable)
EXPOSE 8000

CMD ["python", "-c", "import uvicorn; import os; uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)))"]
