# =============================================================================
# Terra Viva Backend - Dockerfile
# Django 6.0 + Python 3.13
# =============================================================================
# Multi-stage build for optimized production images
# Reference: https://docs.docker.com/build/building/best-practices/

# -----------------------------------------------------------------------------
# Stage 1: Builder
# Build Python wheels to avoid compiling in production image
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS builder

WORKDIR /build

# Install build dependencies for psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements/base.txt requirements.txt

# Build wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Production
# Minimal image with only runtime dependencies
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS production

# Metadata
LABEL maintainer="Terra Viva Team"
LABEL version="0.5.0"
LABEL description="Terra Viva Backend - Django REST API"

# Environment variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
# Disable pip version check for faster builds
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Application directory
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy wheels from builder and install
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# Create non-root user with UID > 10000 for security
# Reference: https://github.com/dnaprawa/dockerfile-best-practices
RUN groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid appgroup --shell /bin/bash --create-home appuser

# Copy application code
COPY --chown=appuser:appgroup . .

# Create directories for static and media files
RUN mkdir -p staticfiles media \
    && chown -R appuser:appgroup staticfiles media

# Copy and set permissions for entrypoint script
COPY --chown=appuser:appgroup docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER appuser

# Collect static files (can be overridden at runtime)
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/api/v1/latest-products/ || exit 1

# Entrypoint and default command
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-"]
