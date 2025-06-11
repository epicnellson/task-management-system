#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3-pip python3-venv nginx redis-server postgresql postgresql-contrib

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up PostgreSQL
echo "Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE taskmanager;"
sudo -u postgres psql -c "CREATE USER taskmanager WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager;"

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Set up Nginx
echo "Setting up Nginx..."
sudo cp nginx/taskmanager.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/taskmanager.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service
echo "Setting up systemd service..."
sudo cp systemd/taskmanager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable taskmanager
sudo systemctl start taskmanager

# Set up SSL with Let's Encrypt
echo "Setting up SSL..."
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

echo "Deployment completed successfully!" 