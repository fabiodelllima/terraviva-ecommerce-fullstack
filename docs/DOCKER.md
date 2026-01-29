# DOCKER

**Versão:** 0.5.0

---

## Visão Geral

O projeto utiliza Docker para garantir consistência entre ambientes de desenvolvimento e produção. A containerização segue as melhores práticas oficiais do Docker, incluindo multi-stage builds, non-root users e health checks.

---

## Arquitetura

O ambiente Docker consiste em três serviços que trabalham em conjunto para fornecer a stack completa da aplicação. O PostgreSQL armazena dados persistentes, o Django serve a API REST, e o Nginx entrega a Single Page Application.

```
┌────────────────────────────────────────────────────────┐
│                frontend-network                        │
│  ┌──────────────┐              ┌──────────────┐        │
│  │   frontend   │<────────────>│   backend    │        │
│  │   (nginx)    │     :8000    │   (django)   │        │
│  └──────────────┘              └──────┬───────┘        │
│         :80                           │                │
└───────────────────────────────────────┼────────────────┘
                                        │
┌───────────────────────────────────────┼────────────────┐
│                backend-network        │                │
│                               ┌───────v───────┐        │
│                               │      db       │        │
│                               │  (postgres)   │        │
│                               └───────────────┘        │
│                                    :5432               │
└────────────────────────────────────────────────────────┘
```

O frontend não tem acesso direto ao banco de dados. Esta separação em networks isoladas aumenta a segurança da aplicação.

---

## Estrutura de Arquivos

| Arquivo                                  | Função                              |
| ---------------------------------------- | ----------------------------------- |
| `compose.yaml`                           | Orquestração para desenvolvimento   |
| `compose.prod.yaml`                      | Override com configurações produção |
| `.dockerignore`                          | Exclusões do contexto de build      |
| `terraviva/backend/Dockerfile`           | Imagem Django multi-stage           |
| `terraviva/backend/docker-entrypoint.sh` | Migrations e collectstatic          |
| `terraviva/frontend/Dockerfile`          | Imagem Vue.js + Nginx multi-stage   |
| `terraviva/frontend/nginx.conf`          | Configuração SPA routing            |

---

## Serviços

| Serviço  | Imagem Base        | Porta | Health Check                  |
| -------- | ------------------ | ----- | ----------------------------- |
| db       | postgres:16-alpine | 5432  | pg_isready                    |
| backend  | python:3.13-slim   | 8000  | curl /api/v1/latest-products/ |
| frontend | nginx:alpine       | 80    | wget localhost                |

---

## Desenvolvimento

O ambiente de desenvolvimento monta o código fonte como volume, permitindo hot reload automático. O PostgreSQL local elimina dependência de serviços externos durante o desenvolvimento.

```bash
# Iniciar todos os serviços
docker compose up --build

# Acessar
# Frontend: http://localhost
# Backend:  http://localhost:8000

# Comandos úteis
docker compose logs -f backend
docker compose exec backend python manage.py createsuperuser
docker compose down -v
```

---

## Produção

O arquivo `compose.prod.yaml` sobrescreve configurações para ambiente de produção. O Gunicorn substitui o runserver, resource limits são aplicados, e logging estruturado é habilitado.

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

| Aspecto   | Desenvolvimento     | Produção              |
| --------- | ------------------- | --------------------- |
| Servidor  | Django runserver    | Gunicorn              |
| Debug     | True                | False                 |
| Volumes   | Código montado      | Apenas dados          |
| Static    | Servido pelo Django | Coletado + Whitenoise |
| Resources | Ilimitado           | Limites definidos     |

---

## Best Practices Aplicadas

| Prática            | Implementação                                      |
| ------------------ | -------------------------------------------------- |
| Multi-stage builds | Builder compila, production executa                |
| Non-root user      | UID 10001 em todos os containers                   |
| Layer caching      | requirements.txt copiado antes do código           |
| Health checks      | Verificação real da aplicação, não apenas processo |
| Networks isoladas  | Backend e frontend em redes separadas              |

---

## Volumes

| Volume         | Propósito                      |
| -------------- | ------------------------------ |
| postgres_data  | Persistência do banco de dados |
| backend_static | Arquivos estáticos coletados   |
| backend_media  | Uploads de usuários            |

---

**Última revisão:** 29/01/2026
