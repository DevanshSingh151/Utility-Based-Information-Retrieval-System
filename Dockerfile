FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p data models docs

COPY . .

# Expose port
EXPOSE 5000

ENV FLASK_ENV=production

# The container entry point uses manage.py for setup and then run.py
CMD python manage.py setup && python run.py
