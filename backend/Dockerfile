FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (fly.io will set PORT env variable)
EXPOSE 8000

# Run with production settings (no reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
