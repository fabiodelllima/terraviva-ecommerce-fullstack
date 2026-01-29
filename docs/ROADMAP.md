# ROADMAP

**Versão:** 0.3.0

---

## Visão Geral

Transformar projeto acadêmico de 2021 em portfólio profissional de produção com stack moderna e deploy funcional.

### Objetivos

| Objetivo                  | Status    | Prioridade |
| ------------------------- | --------- | ---------- |
| Deploy funcional (back)   | CONCLUÍDO | CRÍTICO    |
| Deploy funcional (front)  | CONCLUÍDO | CRÍTICO    |
| Storage persistente       | CONCLUÍDO | CRÍTICO    |
| Validação end-to-end      | CONCLUÍDO | CRÍTICO    |
| Modernizar stack          | PARCIAL   | ALTO       |
| Eliminar vulnerabilidades | CONCLUÍDO   | ALTO       |
| Implementar testes        | PENDENTE  | MÉDIO      |
| CI/CD automatizado        | PENDENTE  | BAIXO      |

---

## Estado Atual

### Backend (Django 5.2.10 + Python 3.14)

- [x] Python 3.14 compatível
- [x] Django 5.2.10 atualizado
- [x] SECRET_KEY em variável de ambiente
- [x] Deploy funcional (Render.com)
- [x] PostgreSQL (Supabase)
- [x] Storage persistente (Supabase Storage)
- [ ] Testes automatizados (Fase 2)

### Frontend (Vue.js 3.5.13 + Vite)

- [x] Vulnerabilidades eliminadas (68 => 0)
- [x] Deploy funcional (Vercel)
- [x] Validação end-to-end
- [x] Migração para Vite
- [ ] Testes automatizados (Fase 2)

### Infraestrutura

- [x] Backend: Render.com
- [x] Frontend: Vercel
- [x] Database: Supabase PostgreSQL
- [x] Storage: Supabase Storage (CDN)
- [ ] CI/CD GitHub Actions (Fase 3)

---

## Fase 1: Restauração - CONCLUÍDA (100%)

**Período:** Janeiro 2026

### Backend - CONCLUÍDO

- [x] Adicionar gunicorn
- [x] Configurar dj-database-url
- [x] Mover secrets para env vars
- [x] Deploy Render.com
- [x] Supabase Storage integration
- [x] Django 5.2.10 (Python 3.14 fix)

### Frontend - CONCLUÍDO

- [x] Atualizar axios para usar env var
- [x] Configurar vercel.json (SPA routing)
- [x] Deploy Vercel
- [x] Validação end-to-end

---

## Fase 2: Modernização

**Período:** Fevereiro-Março 2026

### Frontend

- [x] Migração Vue CLI para Vite
- [x] Vue.js 3.2 para 3.5+
- [ ] Vuex para Pinia
- [x] Resolver 8 CVEs restantes (0 vulnerabilidades)
- [ ] Testes Vitest (>90% coverage)

### Backend

- [ ] pytest + pytest-django
- [ ] Coverage >90%
- [ ] ruff (linter)
- [ ] mypy (type hints)

### Documentação

- [ ] docs/BUSINESS_RULES.md
- [ ] docs/DEPLOYMENT.md
- [ ] ADRs em docs/decisions/

---

## Fase 3: Produção

**Período:** Abril 2026+

### Infraestrutura

- [ ] CI/CD GitHub Actions
- [ ] Sentry (error tracking)
- [ ] Logs estruturados

### Features

- [ ] Dashboard admin customizado
- [ ] Relatórios vendas
- [ ] Filtros avançados

---

## Cronograma

| Fase   | Duração     | Período      | Status    |
| ------ | ----------- | ------------ | --------- |
| Fase 1 | 2 semanas   | Jan 2026     | CONCLUÍDA |
| Fase 2 | 4-6 semanas | Fev-Mar 2026 | PLANEJADA |
| Fase 3 | Contínuo    | Abr+ 2026    | PLANEJADA |

---

## Decisões de Infraestrutura

### ADR-001: Separação Backend/Frontend

Separar completamente em deployments independentes (API REST + SPA).

### ADR-002: Render.com para Backend

Free tier com 750h/mês, SSL automático, deploy via Git.

### ADR-003: Supabase para Database e Storage

PostgreSQL 500MB + Storage 1GB com CDN global. Stack unificado.

### ADR-004: Vercel para Frontend

Migrado de Netlify. 6000 build minutes/mês (vs 300 Netlify), CDN global.

---

**Última revisão:** 29/01/2026
