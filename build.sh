#!/usr/bin/env bash
set -o errexit

echo "==================================="
echo "Starting Build Process..."
echo "==================================="

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "==================================="
echo "Building Tailwind CSS..."
echo "==================================="
cd theme/static_src

npm install

npm run build

cd ../..

echo "==================================="
echo "Verifying Tailwind build..."
echo "==================================="
if [ -f "theme/static/css/dist/styles.css" ]; then
    echo "✓ Tailwind CSS built successfully"
    ls -lh theme/static/css/dist/styles.css
else
    echo "✗ ERROR: Tailwind CSS build failed"
    exit 1
fi

echo "==================================="
echo "Collecting static files..."
echo "==================================="
python manage.py collectstatic --no-input --clear

echo "==================================="
echo "Verifying static files collection..."
echo "==================================="
if [ -f "staticfiles/css/dist/styles.css" ]; then
    echo "✓ Static files collected successfully"
    ls -lh staticfiles/css/dist/styles.css
else
    echo "⚠ Warning: styles.css not found in staticfiles"
fi

echo "==================================="
echo "Running database migrations..."
echo "==================================="
python manage.py migrate

echo "==================================="
echo "Build completed successfully!"
echo "==================================="