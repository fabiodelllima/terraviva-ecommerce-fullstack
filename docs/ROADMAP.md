# ROADMAP

**Versão:** 0.6.0

---

## Visão Geral

O objetivo é transformar um projeto acadêmico de 2021 em case para portfólio profissional com foco em desenvolvimento full-stack, DevOps e arquitetura de software. O roadmap está organizado em fases incrementais, cada uma agregando valor demonstrável ao projeto.

---

## Fase 1: Restauração - Concluída

**Período:** Janeiro 2026

A primeira fase focou em tornar o projeto funcional novamente após 4 anos sem manutenção. Isso envolveu migração de infraestrutura, atualização de dependências e resolução de incompatibilidades.

- [x] Deploy backend (Render.com)
- [x] Deploy frontend (Vercel)
- [x] Database PostgreSQL (Supabase)
- [x] Storage persistente (Supabase Storage)
- [x] Django 6.0.1
- [x] Validação end-to-end

---

## Fase 2: Modernização - Concluída

**Período:** Janeiro 2026

A segunda fase modernizou o tooling e eliminou débito técnico acumulado. A migração para Vite melhorou drasticamente a experiência de desenvolvimento, e a reorganização em monorepo estabeleceu base sólida para evolução.

- [x] Migração Vue CLI para Vite
- [x] Vue.js 3.2 para 3.5+
- [x] Bulma 0.9.4 para 1.0.2
- [x] Vulnerabilidades: 68 → 0
- [x] Reorganização estrutura (monorepo)

---

## Fase 3: DevOps Foundation - Concluída

**Período:** Janeiro 2026

Esta fase estabeleceu a infraestrutura de DevOps necessária para desenvolvimento profissional. Containerização garante consistência entre ambientes, CI/CD automatiza validações, e ferramentas de qualidade mantêm padrões de código.

### Containerização - Concluída

- [x] Dockerfile (backend) - Multi-stage, non-root user
- [x] Dockerfile (frontend) - Multi-stage, Nginx Alpine
- [x] compose.yaml (desenvolvimento)
- [x] compose.prod.yaml (produção)
- [x] .dockerignore (raiz e serviços)
- [x] docker-entrypoint.sh (migrations/collectstatic)
- [x] nginx.conf (SPA routing, gzip, cache)
- [x] docs/DOCKER.md

### CI/CD - Concluída

- [x] GitHub Actions workflow (4 jobs paralelos)
- [x] Backend: Ruff lint + Pyright type check
- [x] Backend: pytest com PostgreSQL service
- [x] Frontend: ESLint + Prettier
- [x] Frontend: Vite build validation
- [ ] Branch protection rules
- [ ] Deploy automatizado

### Qualidade de Código - Concluída

- [x] Ruff (linter + formatter Python)
- [x] Pyright (type checking)
- [x] ESLint 9 + eslint-plugin-vue
- [x] Prettier (formatação de código)
- [x] pre-commit hooks configurados
- [x] pytest-django + pytest-cov

### Segurança - Concluída

- [x] 5 CVEs corrigidos (djoser, simplejwt, Jinja2, requests, social-auth)
- [x] Dependabot monitoramento ativo

---

## Fase 4: Testes & Refatoração - Em Andamento

**Período:** Fevereiro 2026

Esta fase expande a cobertura de testes e implementa padrões arquiteturais. O objetivo é atingir >80% de cobertura no backend e >60% no frontend, aplicando princípios de Clean Architecture.

### Testes

- [x] pytest + pytest-django configurado
- [x] Smoke tests básicos (4 testes)
- [ ] Testes unitários para models
- [ ] Testes unitários para serializers
- [ ] Testes de integração para endpoints
- [ ] Coverage >80% backend
- [ ] Vitest (frontend)
- [ ] Coverage >60% frontend

### Refatoração

- [ ] Service Layer pattern
- [ ] Repository pattern
- [ ] Aplicação de princípios SOLID
- [ ] Expansão de type hints

### Documentação

- [ ] Documentação da API (drf-spectacular)
- [ ] Documentação de regras de negócio
- [ ] Architecture Decision Records (ADRs)

---

## Fase 5: UX/UI Refresh

**Período:** Março 2026

Esta fase renova a interface visual do projeto, aplicando princípios modernos de design e garantindo acessibilidade. O objetivo é atingir score superior a 90 no Lighthouse.

- [ ] Redesign visual
- [ ] Design system documentado
- [ ] Acessibilidade (WCAG 2.1)
- [ ] Lighthouse score >90
- [ ] Loading/error/empty states
- [ ] Melhorias de responsividade

---

## Fase 6: API Evolution

**Período:** Abril 2026

A sexta fase evolui a API REST para GraphQL, oferecendo flexibilidade para o frontend e demonstrando conhecimento em diferentes paradigmas de API. A migração de Vuex para Pinia moderniza o gerenciamento de estado.

- [ ] GraphQL (graphene-django)
- [ ] Apollo Client
- [ ] Vuex para Pinia
- [ ] TypeScript (adoção gradual)

---

## Fase 7: Observabilidade

**Período:** Maio 2026

Esta fase implementa observabilidade abrangente para monitoramento em produção. Error tracking, logging estruturado e coleta de métricas permitem detecção proativa de problemas.

- [ ] Sentry (error tracking)
- [ ] Health check endpoints
- [ ] Structured logging (structlog)
- [ ] Prometheus metrics
- [ ] Grafana dashboards

---

## Fase 8: Event-Driven Architecture

**Período:** Junho-Julho 2026

Esta fase introduz processamento assíncrono e arquitetura orientada a eventos. Celery com Redis permite execução de tasks em background, enquanto message brokers possibilitam comunicação desacoplada entre componentes.

- [ ] Celery + Redis
- [ ] Email notifications (async)
- [ ] Background job processing
- [ ] Event sourcing exploration

---

## Fase 9: Infrastructure as Code

**Período:** Agosto 2026

A fase final implementa orquestração de containers com Kubernetes e monitoramento com Prometheus/Grafana. Foco em operações de infraestrutura cloud-native.

- [ ] Kubernetes manifests
- [ ] Helm charts
- [ ] ArgoCD (GitOps)
- [ ] Terraform (cloud resources)

---

## Métricas de Sucesso

| Métrica                  | Atual  | Meta         |
| ------------------------ | ------ | ------------ |
| Test Coverage (Backend)  | 30%    | >80%         |
| Test Coverage (Frontend) | 0%     | >60%         |
| Vulnerabilities          | 0      | 0            |
| Lighthouse Score         | ~70    | >90          |
| CI Pipeline Time         | ~2min  | <3min        |
| Deploy Time              | Manual | <5min (auto) |

---

**Última revisão:** 30/01/2026
