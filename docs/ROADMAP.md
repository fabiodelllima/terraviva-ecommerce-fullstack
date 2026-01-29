# ROADMAP

**Versão:** 0.4.0

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

## Fase 3: DevOps Foundation

**Período:** Fevereiro 2026

Esta fase estabelece a infraestrutura de DevOps necessária para desenvolvimento profissional. Containerização garante consistência entre ambientes, CI/CD automatiza validações, e observabilidade permite monitorar a aplicação em produção.

### Containerização

- [ ] Dockerfile (backend)
- [ ] Dockerfile (frontend)
- [ ] docker-compose.yml (ambiente dev)
- [ ] .dockerignore

### CI/CD

- [ ] GitHub Actions: lint + tests
- [ ] GitHub Actions: build + deploy
- [ ] Branch protection rules

### Observabilidade

- [ ] Sentry (error tracking)
- [ ] Health check endpoints
- [ ] Structured logging

---

## Fase 4: Qualidade de Código

**Período:** Março 2026

A quarta fase implementa práticas de qualidade de código através de testes automatizados, linting e análise estática. O objetivo é atingir cobertura superior a 90% no backend e 80% no frontend.

### Testing

- [ ] pytest + pytest-django
- [ ] Coverage >90% backend
- [ ] Vitest (frontend)
- [ ] Cypress (e2e)
- [ ] Coverage >80% frontend

### Code Quality

- [ ] ruff (linter Python)
- [ ] mypy (type hints)
- [ ] ESLint + Prettier
- [ ] pre-commit hooks

### Refatoração

- [ ] Service Layer pattern
- [ ] Repository pattern
- [ ] SOLID principles

---

## Fase 5: UX/UI Refresh

**Período:** Abril 2026

Esta fase renova a interface visual do projeto, aplicando princípios modernos de design e garantindo acessibilidade. O objetivo é atingir score superior a 90 no Lighthouse.

- [ ] Redesign visual
- [ ] Design system documentado
- [ ] Acessibilidade (WCAG 2.1)
- [ ] Lighthouse score >90
- [ ] Loading/error/empty states

---

## Fase 6: API Evolution

**Período:** Maio 2026

A sexta fase evolui a API REST para GraphQL, oferecendo flexibilidade para o frontend e demonstrando conhecimento em diferentes paradigmas de API. A migração de Vuex para Pinia moderniza o gerenciamento de estado.

- [ ] GraphQL (graphene-django)
- [ ] Apollo Client
- [ ] Vuex para Pinia
- [ ] TypeScript (gradual)

---

## Fase 7: Event-Driven Architecture

**Período:** Junho-Julho 2026

Esta fase introduz processamento assíncrono e arquitetura orientada a eventos. Celery com Redis permite execução de tasks em background, enquanto message brokers possibilitam comunicação desacoplada entre componentes.

- [ ] Celery + Redis
- [ ] Email notifications (async)
- [ ] RabbitMQ
- [ ] Kafka (exploração)

---

## Fase 8: Infrastructure as Code

**Período:** Agosto 2026

A fase final implementa orquestração de containers com Kubernetes e monitoramento com Prometheus/Grafana. Foco em operações de infraestrutura cloud-native.

- [ ] Kubernetes manifests
- [ ] Helm charts
- [ ] Prometheus + Grafana
- [ ] ArgoCD (GitOps)

---

## Métricas de Sucesso

| Métrica                  | Atual  | Meta         |
| ------------------------ | ------ | ------------ |
| Test Coverage (Backend)  | 0%     | >90%         |
| Test Coverage (Frontend) | 0%     | >80%         |
| Vulnerabilities          | 0      | 0            |
| Lighthouse Score         | ~70    | >90          |
| Deploy Time              | Manual | <5min (auto) |

---

**Última revisão:** 29/01/2026
