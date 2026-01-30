#!/bin/bash
# =============================================================================
# Terra Viva Backend - Docker Entrypoint
# =============================================================================
# This script runs before the main application command.
# It handles database migrations and static file collection.

set -e

# -----------------------------------------------------------------------------
# Wait for database (if DATABASE_URL is set)
# -----------------------------------------------------------------------------
if [ -n "$DATABASE_URL" ]; then
    echo "[INFO] Waiting for database connection..."

    # Extract host and port from DATABASE_URL
    # Format: postgres://user:pass@host:port/dbname
    if [[ "$DATABASE_URL" =~ @([^:]+):([0-9]+)/ ]]; then
        DB_HOST="${BASH_REMATCH[1]}"
        DB_PORT="${BASH_REMATCH[2]}"

        # Wait up to 30 seconds for database
        for i in {1..30}; do
            if python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$DB_HOST', $DB_PORT)); s.close()" 2>/dev/null; then
                echo "[OK] Database is available"
                break
            fi
            echo "[INFO] Waiting for database... ($i/30)"
            sleep 1
        done
    fi
fi

# -----------------------------------------------------------------------------
# Run migrations (production only)
# -----------------------------------------------------------------------------
if [ "$DJANGO_ENV" = "production" ] || [ "$DEBUG" = "False" ]; then
    echo "[INFO] Running database migrations..."
    python manage.py migrate --noinput
    echo "[OK] Migrations completed"
fi

# -----------------------------------------------------------------------------
# Collect static files (production only)
# -----------------------------------------------------------------------------
if [ "$DJANGO_ENV" = "production" ] || [ "$DEBUG" = "False" ]; then
    echo "[INFO] Collecting static files..."
    python manage.py collectstatic --noinput --clear
    echo "[OK] Static files collected"
fi

# -----------------------------------------------------------------------------
# Execute main command
# -----------------------------------------------------------------------------
echo "[INFO] Starting application..."
exec "$@"
