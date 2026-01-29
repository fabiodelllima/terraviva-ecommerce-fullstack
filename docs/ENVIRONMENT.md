# ENVIRONMENT

**Versão:** 0.4.0

---

## Visão Geral

O projeto utiliza variáveis de ambiente para configurações sensíveis, seguindo a metodologia 12-Factor App. Todas as credenciais são gerenciadas via arquivos `.env` localmente e variáveis de ambiente nos serviços de deploy.

---

## Variáveis de Ambiente

### Django Core

| Variável        | Obrigatória | Padrão                | Descrição                  |
| --------------- | ----------- | --------------------- | -------------------------- |
| `SECRET_KEY`    | Sim         | -                     | Chave criptográfica Django |
| `DEBUG`         | Não         | `False`               | Modo debug                 |
| `ALLOWED_HOSTS` | Não         | `localhost,127.0.0.1` | Hosts permitidos           |

### Database

| Variável       | Obrigatória | Padrão                 | Descrição                    |
| -------------- | ----------- | ---------------------- | ---------------------------- |
| `DATABASE_URL` | Não         | `sqlite:///db.sqlite3` | Connection string PostgreSQL |

### Supabase Storage

| Variável                  | Obrigatória | Padrão  | Descrição               |
| ------------------------- | ----------- | ------- | ----------------------- |
| `SUPABASE_URL`            | Não         | -       | URL do projeto Supabase |
| `SUPABASE_SERVICE_KEY`    | Não         | -       | Service role key        |
| `SUPABASE_STORAGE_BUCKET` | Não         | `media` | Nome do bucket          |

### Stripe

| Variável            | Obrigatória | Padrão | Descrição            |
| ------------------- | ----------- | ------ | -------------------- |
| `STRIPE_SECRET_KEY` | Não         | -      | Chave secreta Stripe |
| `STRIPE_PUBLIC_KEY` | Não         | -      | Chave pública Stripe |

### CORS

| Variável               | Obrigatória | Padrão                  | Descrição          |
| ---------------------- | ----------- | ----------------------- | ------------------ |
| `CORS_ALLOWED_ORIGINS` | Não         | `http://localhost:8080` | Origens permitidas |

---

## Configuração por Ambiente

### Desenvolvimento Local

```bash
# terraviva/backend/.env
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

```bash
# terraviva/frontend/.env
VITE_API_URL=http://localhost:8000
```

### Produção (Render)

```bash
SECRET_KEY=<chave-segura-gerada>
DEBUG=False
ALLOWED_HOSTS=terraviva-api-bg8s.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>
SUPABASE_STORAGE_BUCKET=media
STRIPE_SECRET_KEY=sk_live_xxx
CORS_ALLOWED_ORIGINS=https://terraviva.vercel.app
```

### Produção (Vercel)

```bash
VITE_API_URL=https://terraviva-api-bg8s.onrender.com
```

---

## Gerando SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Checklist de Segurança

- [x] `.env` no `.gitignore`
- [x] `SECRET_KEY` única para produção
- [x] `DEBUG=False` em produção
- [x] `ALLOWED_HOSTS` restrito
- [x] `SUPABASE_SERVICE_KEY` nunca no frontend
- [x] HTTPS habilitado em produção

---

**Última revisão:** 29/01/2026
