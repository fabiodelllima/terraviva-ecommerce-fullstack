# ARCHITECTURE

**Versão:** 0.3.0

---

## Visão Geral

Arquitetura Full-Stack Separada:

- Backend: Django REST API
- Frontend: Vue.js SPA
- Database: Supabase PostgreSQL
- Storage: Supabase Storage (CDN)

---

## Estrutura de Diretórios

```
terraviva-ecommerce-fullstack/
├── docs/                           # Documentação
│   ├── ARCHITECTURE.md
│   ├── ENVIRONMENT.md
│   └── ROADMAP.md
│
├── terraviva/
│   ├── backend/
│   │   ├── apps/
│   │   │   ├── order/              # App: Pedidos
│   │   │   │   ├── models.py       # Order, OrderItem
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── urls.py
│   │   │   └── product/            # App: Produtos
│   │   │       ├── models.py       # Product, Category
│   │   │       ├── views.py
│   │   │       ├── serializers.py
│   │   │       └── urls.py
│   │   ├── config/
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── storage.py          # Supabase Storage backend
│   │   ├── requirements/
│   │   │   └── base.txt
│   │   ├── static/
│   │   ├── media/
│   │   └── manage.py
│   │
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   ├── views/
│       │   ├── router/
│       │   ├── store/
│       │   └── main.js
│       ├── index.html
│       ├── vite.config.js
│       ├── vercel.json
│       └── package.json
│
├── .github/
│   └── workflows/
│       └── keep-alive.yml
│
├── CHANGELOG.md
├── README.md
└── LICENSE
```

---

## Infraestrutura de Produção

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TERRA VIVA INFRASTRUCTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│         ┌──────────────────┐       ┌──────────────────┐                 │
│         │     VERCEL       │       │    RENDER.COM    │                 │
│         │   ────────────   │       │   ────────────   │                 │
│         │   Vue.js SPA     │◄─────►│   Django API     │                 │
│         │   CDN Global     │       │   gunicorn       │                 │
│         └──────────────────┘       └────────┬─────────┘                 │
│                                             │                           │
│                              ┌──────────────┴──────────────┐            │
│                              ▼                             ▼            │
│                   ┌──────────────────┐         ┌──────────────────┐     │
│                   │    SUPABASE      │         │    SUPABASE      │     │
│                   │    PostgreSQL    │         │    Storage       │     │
│                   │   500MB free     │         │   1GB free       │     │
│                   └──────────────────┘         │   CDN (285 POPs) │     │
│                                                └──────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### URLs de Produção

| Serviço     | URL                                     |
| ----------- | --------------------------------------- |
| Frontend    | https://terraviva.vercel.app            |
| Backend API | https://terraviva-api-bg8s.onrender.com |

---

## Stack Tecnológico

| Camada            | Tecnologia            | Versão |
| ----------------- | --------------------- | ------ |
| Backend Runtime   | Python                | 3.14   |
| Backend Framework | Django                | 6.0.1  |
| API               | Django REST Framework | 3.15.2 |
| Auth              | djoser                | 2.2.3  |
| Storage           | supabase-py           | 2.27.1 |
| Payments          | Stripe                | 11.3.0 |
| Frontend          | Vue.js                | 3.5.13 |
| Build Tool        | Vite                  | 6.4.1  |
| State             | Vuex                  | 4.1.0  |
| CSS               | Bulma                 | 1.0.2  |

---

## Storage Architecture

### Custom Storage Backend

```python
# terraviva/backend/config/storage.py
class SupabaseStorage(Storage):
    """
    Custom Django storage backend for Supabase Storage.
    - Upload direto para bucket Supabase
    - URLs públicas via CDN
    - Fallback para imagens legadas
    """
```

### Estrutura do Bucket

```
media/                          # Bucket Supabase
└── uploads/
    ├── produto1.jpg
    ├── produto1_thumb.jpg
    └── ...
```

### Limitações do Supabase Storage

**Nomes de arquivo:** O Supabase Storage não aceita caracteres especiais (acentos, cedilha, etc.) em nomes de arquivo. Utilize apenas caracteres ASCII:

- Correto: `maca.jpg`, `limao.jpg`, `acai.jpg`
- Incorreto: `maçã.jpg`, `limão.jpg`, `açaí.jpg`

---

## Deploy Configuration

### Render (Backend)

- **Root Directory:** `terraviva/backend`
- **Build Command:** `pip install -r requirements/base.txt`
- **Start Command:** `gunicorn config.wsgi:application`

### Vercel (Frontend)

- **Root Directory:** `terraviva/frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variable:** `VITE_API_URL=https://terraviva-api-bg8s.onrender.com`

---

**Última revisão:** 29/01/2026
