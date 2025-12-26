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

npm ci --only=production 2>/dev/null || npm install

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
echo "Verifying static files..."
echo "==================================="
if [ -d "staticfiles/css" ]; then
    echo "✓ Static files collected"
    ls -lh staticfiles/css/dist/styles.css 2>/dev/null || echo "⚠ styles.css not in expected location"
else
    echo "⚠ staticfiles/css directory not found"
fi

echo "==================================="
echo "Running database migrations..."
echo "==================================="
python manage.py migrate --no-input

echo "==================================="
echo "Build completed successfully! 🎉"
echo "==================================="