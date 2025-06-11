FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE $PORT

# Start the application
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - app:create_app() 