# CHANGELOG

All notable changes to the Terra Viva project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.6.0] - 2026-01-30

### Context

Complete CI/CD implementation with GitHub Actions, security vulnerability fixes, code quality tooling setup (linting, formatting, type checking), and automated test addition.

### Added

- **CI/CD Pipeline (GitHub Actions)**
  - Workflow `.github/workflows/ci.yml` with 4 parallel jobs
  - Backend Lint: Ruff (linter + formatter) + Pyright (type checking)
  - Backend Test: pytest with PostgreSQL 16-alpine service container
  - Frontend Lint: ESLint + Prettier
  - Frontend Build: Vite production build

- **Quality Tools - Backend**
  - Ruff configured in `pyproject.toml` (DJ, B, UP, I rules)
  - Pyright for type checking with Django-friendly rules
  - pytest-django with coverage reporting
  - `config/settings_test.py` for SQLite-based testing

- **Quality Tools - Frontend**
  - ESLint 9 with eslint-plugin-vue (flat config)
  - Prettier with eslint-config-prettier integration
  - Scripts: `lint`, `lint:fix`, `format`, `format:check`

- **Pre-commit Hooks**
  - `.pre-commit-config.yaml` with Ruff, Pyright, ESLint, Prettier
  - General hooks: trailing-whitespace, end-of-file-fixer

- **Automated Tests**
  - `apps/product/tests.py`: smoke tests for product endpoints
  - `apps/order/tests.py`: smoke tests for order endpoints
  - `api_client` fixture in `conftest.py`

### Changed

- **Backend Code Quality**
  - Imports organized (isort via Ruff)
  - Trailing whitespace and newlines fixed
  - Exception chaining with `raise from None`
  - Modernized f-strings and format specifiers
  - `warnings.warn()` with stacklevel=2

- **Frontend Code Quality**
  - Code formatted with Prettier (single quotes, no semicolons)
  - Unused imports removed
  - Unused variables prefixed with underscore

### Security

- **Dependencies Updated (5 CVEs fixed)**
  - djoser: 2.2.3 → 2.3.0 (CVE-2024-21543: Authentication Bypass)
  - djangorestframework-simplejwt: 5.3.1 → 5.5.1 (CVE-2024-22513: Privilege Management)
  - Jinja2: 3.1.5 → 3.1.6 (CVE-2025-27516: Sandbox Breakout)
  - requests: 2.32.3 → 2.32.4 (CVE-2024-47081: Credential Leak)
  - social-auth-app-django: 5.4.2 → 5.6.0 (CVE-2025-61783: Unsafe Association)

### Infrastructure

- **CI/CD:** GitHub Actions (4 jobs, ~1-2min total)
- **Linting:** Ruff 0.9.3, ESLint 9.18, Prettier 4.0
- **Type Checking:** Pyright 1.1.391
- **Testing:** pytest 8.3.4, pytest-django 4.9.0, pytest-cov 6.0.0

---

## [0.5.0] - 2026-01-29

### Context

Complete project containerization with Docker and Docker Compose, following official best practices. Establishes foundation for CI/CD and consistent environments between development and production.

### Added

- **Multi-Stage Dockerfiles**
  - `terraviva/backend/Dockerfile` with builder stage for Python wheels
  - `terraviva/frontend/Dockerfile` with Node build stage and Nginx production
  - Non-root users (UID 10001) for security
  - Health checks on all containers

- **Docker Compose**
  - `compose.yaml` for development with hot reload
  - `compose.prod.yaml` with production overrides
  - Isolated networks: `backend-network` and `frontend-network`
  - Named volumes for data persistence

- **Support Configurations**
  - `terraviva/backend/docker-entrypoint.sh` for migrations and collectstatic
  - `terraviva/frontend/nginx.conf` optimized for SPA
  - `.dockerignore` at root and in each service
  - `docs/DOCKER.md` with complete documentation

### Changed

- File structure reorganized to support separate Docker contexts

### Infrastructure

- **PostgreSQL:** 16-alpine with health checks
- **Backend:** Python 3.13-slim + Gunicorn (prod) / runserver (dev)
- **Frontend:** Node 20-alpine (build) + Nginx Alpine (serve)
- **Networks:** backend-network / frontend-network isolation
- **Volumes:** postgres_data, backend_static, backend_media

---

## [0.4.0] - 2026-01-29

### Context

Complete project structure reorganization into monorepo, separating backend and frontend into dedicated directories. Updated all technical documentation to professional standards.

### Added

- Monorepo structure: `terraviva/backend` and `terraviva/frontend`
- `docs/DEPLOYMENT.md` with infrastructure configuration
- Introductory prose in all documentation sections

### Changed

- **Project Structure**
  - `order/`, `product/` => `terraviva/backend/apps/`
  - `terraviva/` (config) => `terraviva/backend/config/`
  - `terraviva_v/` => `terraviva/frontend/`
  - `requirements.txt` => `terraviva/backend/requirements/base.txt`

- **Imports and Configurations**
  - Apps registered as `apps.product`, `apps.order`
  - `DJANGO_SETTINGS_MODULE` updated to `config.settings`
  - All internal imports updated

- **Documentation**
  - README.md with professional sections and prose
  - ARCHITECTURE.md focused on current state
  - ROADMAP.md with detailed phases
  - ENVIRONMENT.md updated for new structure

### Removed

- Obsolete Vue CLI files (`babel.config.js`, `vue.config.js`)
- Flat directory structure at root

---

## [0.3.0] - 2026-01-29

### Context

Complete migration of build system from Vue CLI to Vite, eliminating all frontend vulnerabilities and updating Bulma CSS framework to version 1.0.

### Added

- **Vite Build System**
  - `vite.config.js` with proxy for API in development
  - Support for `import.meta.env` for environment variables
  - Optimized Hot Module Replacement (HMR)
  - Production build ~3s (vs ~30s with Vue CLI)

- **CI/CD Keep-Alive**
  - GitHub Actions workflow for daily Supabase ping
  - Prevents automatic pause due to inactivity (7 days)
  - Render ping to keep service active

### Changed

- **Frontend Dependencies**
  - Vue CLI => Vite 6.4.1
  - Vue: 3.2.13 => 3.5.13
  - Vue Router: 4.0.11 => 4.5.0
  - Vuex: 4.0.2 => 4.1.0
  - Bulma: 0.9.4 => 1.0.2
  - Vulnerabilities: 8 => 0

- **Build Configuration**
  - `index.html` moved to project root (Vite requirement)
  - Imports with explicit `.vue` extension
  - Environment variables: `VUE_APP_*` => `VITE_*`

- **Styles**
  - Fixes for Bulma 1.0 compatibility
  - Color fix for `.is-success` and `.is-outlined` buttons
  - Background fix for active `.navbar-item`
  - Header logo with `display: inline` (spacing fix)

- **Repository**
  - Renamed: `projeto-terraviva` => `terraviva-ecommerce-fullstack`

### Removed

- Vue CLI and plugins (`@vue/cli-service`, `@vue/cli-plugin-*`)
- `babel.config.js` (Vite uses esbuild)
- `vue.config.js` (replaced by `vite.config.js`)
- Deprecated Webpack dependencies

### Fixed

- Spacing in "terraviva" logo in header
- Button and icon colors for Bulma 1.0
- Router using `import.meta.env.BASE_URL`

### Security

- **Frontend:** 0 vulnerabilities (was 8 moderate)
- All dependencies updated to secure versions

### Infrastructure

- **Build:** Vite 6.4.1 (replaced Vue CLI 5.x)
- **Frontend:** Vercel with `VITE_API_URL` configured
- **Repository:** github.com/fabiodelllima/terraviva-ecommerce-fullstack

---

## [2.1.0] - 2026-01-11

### Context

Implementation of persistent media storage via Supabase Storage, solving the ephemeral files problem on Render.com. Includes Django upgrade to version 5.2.10 due to Python 3.14 incompatibilities.

### Added

- **Supabase Storage Integration**
  - Custom storage backend (`terraviva/storage.py`) for Supabase
  - Image upload directly to `media/uploads/` bucket
  - Public URLs via Supabase CDN (285 POPs globally)
  - Graceful fallback for legacy images

- **STORAGES Configuration**
  - Django 5.2+ STORAGES dict for storage management
  - WhiteNoise maintained for static files
  - Supabase for media files (uploads)

### Changed

- **Django Upgrade**
  - Django: 4.2.17 => 5.2.10 (Python 3.14 compatibility)
  - Fixed `AttributeError: 'super' object has no attribute 'dicts'` bug
  - Configuration migrated from `DEFAULT_FILE_STORAGE` to `STORAGES`

- **Product Model**
  - `make_thumbnail()` method fixed (path duplication fix)
  - `get_image()` and `get_thumbnail()` methods with error handling
  - `verbose_name_plural` corrected to "Produtos"

- **Frontend Deploy**
  - Migration from Netlify to Vercel
  - `vercel.json` configuration for SPA routing

- **Dependencies**
  - supabase: 2.27.1 (new)
  - storage3: 2.27.1 (new)
  - Pillow: 12.1.0 (maintained)

### Removed

- `image_url` field from Product model (redundant with Supabase URLs)
- `DEFAULT_FILE_STORAGE` configuration (deprecated Django 5.2)
- Duplicate `STATICFILES_STORAGE` configuration
- `netlify.toml` (migrated to Vercel)
- `Procfile` (was for Heroku, not used)

### Fixed

- Python 3.14 + Django 4.2/5.1 incompatibility (template context bug)
- Path duplication in thumbnails (`uploads/uploads/file.jpg`)
- Error handling for legacy images (404 on Supabase)

### Infrastructure

- **Backend:** Render.com (https://terraviva-api-bg8s.onrender.com)
- **Frontend:** Vercel (https://terraviva.vercel.app)
- **Database:** Supabase PostgreSQL (500MB free tier)
- **Storage:** Supabase Storage (1GB free tier, global CDN)

---

## [2.0.1] - 2026-01-09

### Security

- **CRITICAL:** SECRET_KEY removed from source code and moved to environment variable
- **CRITICAL:** STRIPE_SECRET_KEY removed from source code and moved to environment variable
- DEBUG now configurable via environment (prevents DEBUG=True in production)
- ALLOWED_HOSTS now configurable via environment (prevents host poisoning)
- Security headers configured for production (XSS, CSRF, SSL)

### Added

- python-dotenv for environment variable management
- .env.example as configuration template
- docs/ENVIRONMENT.md with configuration guide

### Changed

- Pillow: 10.4.0 => 12.1.0 (Python 3.14 compatibility)
- .gitignore updated to exclude .env files

### Removed

- django-on-heroku (discontinued)
- Hardcoded secrets from settings.py

---

## [2.0.0] - 2026-01-07

### Context

Beginning of **complete project revitalization** after 4 years without maintenance (2022-2025). The goal is to transform the 2021 academic project into a professional production portfolio case.

### Added

- **Complete Professional Documentation**
  - README.md reformulated with hierarchical methodology
  - docs/ROADMAP.md with Phase 1, 2, 3 planning
  - docs/ARCHITECTURE.md with structural analysis
  - CHANGELOG.md following Keep a Changelog format
  - LICENSE (MIT)
  - docs/ structure created

### Changed

- **Backend Dependencies (Python)**
  - Python: 3.9 => 3.14
  - Django: 4.1.2 => 4.2.17 LTS
  - Pillow: 9.2.0 => 10.4.0
  - psycopg2-binary: 2.9.4 => 2.9.10
  - Django REST Framework: 3.14.0 => 3.15.2
  - djoser: 4.8.0 => 5.3.1
  - Stripe: 4.2.0 => 11.3.0

- **Frontend Dependencies (npm)**
  - Resolved 20 critical/high vulnerabilities
  - Vulnerabilities: 68 => 8 (all moderate, dev-only)

### Security

- Resolved 20 of 28 npm vulnerabilities (68 => 8)
- 8 remaining vulnerabilities: moderate severity, dev-only

---

## [1.0.0] - 2021-12-XX

### Context

Initial release of the **Coding4Hope** academic project. E-commerce platform developed to automate sales for an NGO, replacing manual processes with a complete online system.

### Added

- **Django Backend**
  - Django 4.1.2 + Django REST Framework
  - Apps: `product`, `order`
  - Models: Product, Category, Order, OrderItem
  - Complete REST API (CRUD products, checkout, auth)
  - Integrated admin panel
  - Stripe integration (payments)

- **Vue.js Frontend**
  - Vue.js 3.2.13 + Vue Router + Vuex
  - 10 pages: Home, Product, Category, Search, Cart, Checkout, Success, Login, SignUp, MyAccount
  - Stripe Elements integration
  - CSS framework: Bulma

### Impact

Project successfully delivered to the NGO, demonstrating technical viability and measurable social impact.

---

## Legend

- `Added`: New features
- `Changed`: Changes to existing features
- `Removed`: Removed features
- `Fixed`: Bug fixes
- `Security`: Vulnerability fixes

---

**Last updated:** 2026-01-30
**Current version:** 0.6.0
