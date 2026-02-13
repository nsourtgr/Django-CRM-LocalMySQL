#!/bin/sh

# Αυτόματα migrate χωρίς να ελέγχει MySQL ping
echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8001
