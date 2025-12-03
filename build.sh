#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies and build Tailwind CSS
echo "Building Tailwind CSS..."
cd theme/static_src
npm install
npm run build
cd ../..

# Collect static files (includes the compiled Tailwind CSS)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate