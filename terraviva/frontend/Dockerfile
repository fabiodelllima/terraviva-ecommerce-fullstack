# =============================================================================
# Terra Viva Frontend - Dockerfile
# Vue.js 3 + Vite
# =============================================================================
# Multi-stage build: Node for building, Nginx for serving
# Reference: https://docs.docker.com/build/building/best-practices/

# -----------------------------------------------------------------------------
# Stage 1: Builder
# Build the Vue.js application with Vite
# -----------------------------------------------------------------------------
FROM node:20-alpine AS builder

WORKDIR /build

# Copy package files first for layer caching
COPY package*.json ./

# Install dependencies
RUN npm ci --silent

# Copy source code
COPY . .

# Build argument for API URL (injected at build time)
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=${VITE_API_URL}

# Build the application
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 2: Production
# Serve static files with Nginx
# -----------------------------------------------------------------------------
FROM nginx:alpine AS production

# Metadata
LABEL maintainer="Terra Viva Team"
LABEL version="0.5.0"
LABEL description="Terra Viva Frontend - Vue.js SPA"

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from builder stage
COPY --from=builder /build/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create non-root user for nginx
RUN addgroup -g 10001 -S appgroup \
    && adduser -u 10001 -S appuser -G appgroup \
    && chown -R appuser:appgroup /usr/share/nginx/html \
    && chown -R appuser:appgroup /var/cache/nginx \
    && chown -R appuser:appgroup /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown -R appuser:appgroup /var/run/nginx.pid

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Run as non-root user
USER appuser

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
