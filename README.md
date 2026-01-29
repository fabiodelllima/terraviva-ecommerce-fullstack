# Terra Viva

![Status](https://img.shields.io/badge/Status-Em%20Produção-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.0.1-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3.5.13-brightgreen)
![Vite](https://img.shields.io/badge/Vite-6.4.1-purple)
![Vulnerabilities](https://img.shields.io/badge/Vulnerabilities-0-success)
![License](https://img.shields.io/badge/License-MIT-blue)

E-commerce full-stack para produtos orgânicos. Catálogo, carrinho, checkout com Stripe e gestão de pedidos.

**[Ver Demo](https://terraviva.vercel.app)** · **[API](https://terraviva-api-bg8s.onrender.com/api/v1/latest-products/)**

> Projeto acadêmico (Coding4Hope, 2021) revitalizado em 2026 como case de portfólio.

---

## Índice

- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Infraestrutura](#infraestrutura)
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
| Stripe (pagamentos)   | Axios 1.9.0   |                        |

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

### Vercel (Frontend)

Hospeda a SPA Vue.js com distribuição global via CDN. Build automático a cada push na branch main, com preview deployments para pull requests. SSL automático e edge caching para assets estáticos.

### Render (Backend)

Executa a API Django com gunicorn em container gerenciado. Auto-deploy conectado ao GitHub, com spin-down automático no plano gratuito (cold start ~30s após inatividade).

### Supabase (Database + Storage)

PostgreSQL gerenciado para persistência de dados (produtos, pedidos, usuários). Storage com CDN para imagens de produtos, eliminando necessidade de servir arquivos estáticos pelo Django.

---

## Estrutura

O repositório está organizado em monorepo com separação clara entre backend e frontend dentro do diretório `terraviva/`. Esta estrutura facilita o desenvolvimento local enquanto permite deploys independentes para cada serviço. A documentação técnica fica centralizada em `docs/`.

```
terraviva-ecommerce-fullstack/
├── terraviva/
│   ├── backend/
│   │   ├── apps/
│   │   │   ├── product/       # Catálogo e categorias
│   │   │   └── order/         # Pedidos e checkout
│   │   ├── config/            # Settings, URLs, WSGI
│   │   └── requirements/
│   │
│   └── frontend/
│       ├── src/
│       │   ├── views/         # Páginas
│       │   ├── components/    # Componentes reutilizáveis
│       │   ├── store/         # Vuex (carrinho, auth)
│       │   └── router/
│       └── vite.config.js
│
└── docs/                      # Documentação técnica
```

---

## Desenvolvimento

O ambiente local requer Python 3.14+ e Node.js 18+. Backend e frontend rodam em processos separados, simulando o ambiente de produção. O frontend faz proxy das requisições `/api` para o backend local durante desenvolvimento.

```bash
# Clone
git clone https://github.com/fabiodelllima/terraviva-ecommerce-fullstack.git
cd terraviva-ecommerce-fullstack

# Backend
python -m venv venv && source venv/bin/activate
cd terraviva/backend
pip install -r requirements/base.txt
cp .env.example .env  # Configurar variáveis
python manage.py migrate
python manage.py runserver

# Frontend (outro terminal)
cd terraviva/frontend
npm install
npm run dev
```

Acesse <http://localhost:8080> · Stripe test: `4242 4242 4242 4242`

---

## API

A API REST segue convenções RESTful com versionamento via URL (`/api/v1/`). Endpoints públicos permitem navegação no catálogo, enquanto operações de checkout e histórico requerem autenticação via token. A autenticação é gerenciada pelo djoser com endpoints padrão em `/api/v1/auth/`.

```
GET  /api/v1/latest-products/       Produtos recentes
GET  /api/v1/products/<category>/   Por categoria
POST /api/v1/products/search/       Busca
POST /api/v1/checkout/              Finalizar pedido [AUTH]
GET  /api/v1/orders/                Histórico [AUTH]
```

---

## Documentação

| Documento                               | Conteúdo                  |
| --------------------------------------- | ------------------------- |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Decisões técnicas e stack |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md)     | Configuração de deploy    |
| [ENVIRONMENT.md](docs/ENVIRONMENT.md)   | Variáveis de ambiente     |
| [ROADMAP.md](docs/ROADMAP.md)           | Planejamento do projeto   |
| [CHANGELOG.md](CHANGELOG.md)            | Histórico de versões      |

---

## Licença

[MIT](LICENSE)
