FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command; overridden by docker-compose command, but good fallback
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
