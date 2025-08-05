#!/bin/sh

# Set defaults
SQL_HOST=${SQL_HOST:-db}
SQL_PORT=${SQL_PORT:-5432}

# Wait for PostgreSQL (if specified)
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL is up!"
fi

# Run database migrations
echo "Applying database migrations..."
python src/manage.py migrate --noinput
echo "Migrations applied."

# Collect static files
echo "Collecting static files..."
python src/manage.py collectstatic --noinput
echo "Static files collected."

# Start Gunicorn on 0.0.0.0 so it's accessible from Nginx
echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 &

# Start Nginx in the foreground
echo "Starting Nginx..."
exec nginx -g "daemon off;"
