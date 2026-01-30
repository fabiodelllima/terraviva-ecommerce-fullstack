# Terra Viva

![Status](https://img.shields.io/badge/Status-Em%20Produção-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.0.1-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3.5.13-brightgreen)
![Vite](https://img.shields.io/badge/Vite-6.4.1-purple)
![CI](https://github.com/fabiodelllima/terraviva-ecommerce-fullstack/actions/workflows/ci.yml/badge.svg)
![Vulnerabilities](https://img.shields.io/badge/Vulnerabilities-0-success)
![License](https://img.shields.io/badge/License-MIT-blue)

E-commerce full-stack para produtos orgânicos. Catálogo, carrinho, checkout com Stripe e gestão de pedidos.

**[Ver Demo](https://terraviva.vercel.app)** · **[API](https://terraviva-api-bg8s.onrender.com/api/v1/latest-products/)**

```
╭────────────────────╮
│   T E R R A        │
│       V I V A      │
╰────────────────────╯
```

> Projeto acadêmico (Coding4Hope, 2021) revitalizado em 2026 como case de portfólio.

---

## Sumário

- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Infraestrutura](#infraestrutura)
- [CI/CD](#cicd)
- [Estrutura](#estrutura)
- [Desenvolvimento](#desenvolvimento)
- [API](#api)
- [Documentação](#documentação)

---

## Stack

O backend utiliza Django com Django REST Framework para expor uma API RESTful, autenticação via djoser com tokens JWT, e integração com Stripe para processamento de pagamentos. O frontend é uma Single Page Application em Vue.js 3 com Vuex para gerenciamento de estado e Bulma como framework CSS. A migração de Vue CLI para Vite reduziu o tempo de build de 30s para 3s.

| Backend               | Frontend      | Infraestrutura         |
| --------------------- | ------------- | ---------------------- |
| Python 3.14           | Vue.js 3.5.13 | Render.com (API)       |
| Django 6.0.1          | Vite 6.4.1    | Vercel (SPA)           |
| Django REST Framework | Vuex 4.1.0    | Supabase (PostgreSQL)  |
| djoser (auth)         | Bulma 1.0.2   | Supabase Storage (CDN) |
| Stripe (pagamentos)   | Axios 1.9.0   | GitHub Actions (CI)    |

---

## Arquitetura

A aplicação segue uma arquitetura de microsserviços simplificada com separação completa entre frontend e backend. O browser carrega a SPA do Vercel e faz chamadas REST para a API no Render. O backend persiste dados no PostgreSQL e serve imagens do Supabase Storage via CDN, eliminando a necessidade de gerenciar uploads no servidor.

```
                      ┌─────────────┐
                      │   Browser   │
                      └──────┬──────┘
                             │
               ┌─────────────┴─────────────┐
               v                           v
      ┌─────────────────┐        ┌─────────────────┐
      │     Vercel      │        │     Render      │
      │    Vue.js SPA   │<──────>│   Django API    │
      │    CDN Global   │        │    gunicorn     │
      └─────────────────┘        └────────┬────────┘
                                          │
                            ┌─────────────┴─────────────┐
                            v                           v
                   ┌─────────────────┐        ┌─────────────────┐
                   │    Supabase     │        │    Supabase     │
                   │   PostgreSQL    │        │     Storage     │
                   └─────────────────┘        └─────────────────┘
```

---

## Infraestrutura

O projeto utiliza três serviços cloud gratuitos, cada um otimizado para sua função específica. Esta combinação oferece um ambiente de produção robusto sem custo, ideal para portfólio e projetos de pequeno porte.

### Vercel

Hospeda a SPA Vue.js com distribuição global via CDN. Build automático a cada push na branch main, com preview deployments para pull requests. SSL automático e edge caching para assets estáticos.

### Render

Executa a API Django com gunicorn em container gerenciado. Auto-deploy conectado ao GitHub, com spin-down automático no plano gratuito (cold start ~30s após inatividade).

### Supabase

PostgreSQL gerenciado para persistência de dados (produtos, pedidos, usuários). Storage com CDN para imagens de produtos, eliminando necessidade de servir arquivos estáticos pelo Django.

---

## CI/CD

O projeto utiliza GitHub Actions para integração contínua com 4 jobs paralelos que executam a cada push e pull request nas branches main e develop.

### Jobs do Pipeline

| Job            | Ferramentas        | Propósito               |
| -------------- | ------------------ | ----------------------- |
| Backend Lint   | Ruff, Pyright      | Linting + type checking |
| Backend Test   | pytest, PostgreSQL | Testes unitários        |
| Frontend Lint  | ESLint, Prettier   | Linting + formatação    |
| Frontend Build | Vite               | Validação de build      |

### Ferramentas de Qualidade

**Backend:**

- **Ruff** - Linter e formatter Python (substitui Black, flake8, isort)
- **Pyright** - Type checker estático para Python
- **pytest** - Framework de testes com integração Django

**Frontend:**

- **ESLint** - Linter JavaScript/Vue com flat config
- **Prettier** - Formatter integrado com ESLint

### Pre-commit Hooks

O desenvolvimento local utiliza pre-commit hooks para capturar problemas antes do push:

```bash
pip install pre-commit
pre-commit install
```

---

## Estrutura

O repositório está organizado em monorepo com separação clara entre backend e frontend dentro do diretório `terraviva/`. Esta estrutura facilita o desenvolvimento local enquanto permite deploys independentes para cada serviço. A documentação técnica fica centralizada em `docs/`.

```
terraviva-ecommerce-fullstack/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline CI do GitHub Actions
├── terraviva/
│   ├── backend/
│   │   ├── apps/
│   │   │   ├── product/       # Catálogo e categorias
│   │   │   └── order/         # Pedidos e checkout
│   │   ├── config/            # Configurações Django
│   │   ├── requirements/      # Dependências Python
│   │   ├── Dockerfile         # Build multi-stage
│   │   └── pyproject.toml     # Config Ruff, pytest, coverage
│   └── frontend/
│       ├── src/
│       │   ├── components/    # Componentes Vue
│       │   ├── views/         # Componentes de página
│       │   ├── router/        # Vue Router
│       │   └── store/         # Vuex store
│       ├── Dockerfile         # Build multi-stage
│       └── eslint.config.js   # ESLint flat config
├── docs/                      # Documentação técnica
├── compose.yaml               # Docker Compose (dev)
├── compose.prod.yaml          # Docker Compose (prod)
└── .pre-commit-config.yaml    # Pre-commit hooks
```

---

## Desenvolvimento

### Pré-requisitos

- Python 3.13+
- Node.js 20+
- Docker (opcional)

### Setup Local

**Backend:**

```bash
cd terraviva/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
cp .env.example .env      # Configurar variáveis de ambiente
python manage.py migrate
python manage.py runserver
```

**Frontend:**

```bash
cd terraviva/frontend
npm install
npm run dev
```

### Setup com Docker

```bash
# Desenvolvimento (com hot reload)
docker compose up

# Produção
docker compose -f compose.yaml -f compose.prod.yaml up
```

### Executando Testes

**Backend:**

```bash
cd terraviva/backend
pytest -v                    # Executar testes
pytest --cov=apps            # Com coverage
ruff check .                 # Lint
ruff format --check .        # Verificar formatação
pyright .                    # Type check
```

**Frontend:**

```bash
cd terraviva/frontend
npm run lint                 # ESLint
npm run format:check         # Verificar Prettier
npm run build                # Validar build
```

---

## API

A API REST expõe endpoints para produtos, categorias, pedidos e autenticação. Todos os endpoints são prefixados com `/api/v1/`.

### Endpoints Públicos

| Método | Endpoint                         | Descrição             |
| ------ | -------------------------------- | --------------------- |
| GET    | `/api/v1/latest-products/`       | Últimos 4 produtos    |
| GET    | `/api/v1/products/{cat}/{slug}/` | Detalhes do produto   |
| GET    | `/api/v1/products/{category}/`   | Produtos da categoria |
| POST   | `/api/v1/products/search/`       | Buscar produtos       |

### Endpoints Protegidos

| Método | Endpoint            | Descrição           |
| ------ | ------------------- | ------------------- |
| POST   | `/api/v1/checkout/` | Processar pagamento |
| GET    | `/api/v1/orders/`   | Pedidos do usuário  |

### Autenticação

| Método | Endpoint                | Descrição         |
| ------ | ----------------------- | ----------------- |
| POST   | `/api/v1/users/`        | Registro          |
| POST   | `/api/v1/token/login/`  | Login (get token) |
| POST   | `/api/v1/token/logout/` | Logout            |

---

## Documentação

| Documento                               | Descrição                     |
| --------------------------------------- | ----------------------------- |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Arquitetura do sistema        |
| [ROADMAP.md](docs/ROADMAP.md)           | Roadmap de desenvolvimento    |
| [ENVIRONMENT.md](docs/ENVIRONMENT.md)   | Guia de variáveis de ambiente |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md)     | Instruções de deploy          |
| [DOCKER.md](docs/DOCKER.md)             | Guia de setup Docker          |
| [CHANGELOG.md](CHANGELOG.md)            | Histórico de versões          |

---

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

**Versão:** 0.6.0  
**Última atualização:** 30/01/2026
