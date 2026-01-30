# ARCHITECTURE

**Versão:** 0.5.0

---

## Visão Geral

Terra Viva segue uma arquitetura de aplicação distribuída com separação completa entre frontend e backend. O frontend é uma Single Page Application (SPA) que consome uma API REST. O backend é stateless, permitindo escalabilidade horizontal.

A escolha por serviços cloud separados (Vercel, Render, Supabase) reflete uma arquitetura moderna onde cada componente é otimizado para sua função específica, em contraste com o modelo monolítico tradicional.

---

## Diagrama

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

## Stack Tecnológico

O projeto utiliza ferramentas atualizadas e bem estabelecidas, priorizando produtividade, manutenibilidade e compatibilidade com o ecossistema cloud. A tabela abaixo detalha cada componente e a justificativa de escolha.

| Camada   | Tecnologia            | Versão | Justificativa                           |
| -------- | --------------------- | ------ | --------------------------------------- |
| Runtime  | Python                | 3.14   | Versão mais recente, melhor performance |
| Backend  | Django                | 6.0.1  | Framework maduro, batteries included    |
| API      | Django REST Framework | 3.15.2 | Padrão de facto para APIs Django        |
| Auth     | djoser                | 2.3.0  | Endpoints de auth prontos               |
| Payments | Stripe                | 11.3.0 | Líder de mercado em pagamentos          |
| Frontend | Vue.js                | 3.5.13 | Reativo, progressivo, curva suave       |
| Build    | Vite                  | 6.4.1  | Build rápido, HMR instantâneo           |
| State    | Vuex                  | 4.1.0  | Gerenciamento de estado centralizado    |
| CSS      | Bulma                 | 1.0.2  | CSS-only, sem JS, customizável          |

---

## Padrões Utilizados

### Backend

O backend segue o padrão MVT (Model-View-Template) do Django, adaptado para API REST onde Views funcionam como endpoints e Templates são substituídos por respostas JSON. O fluxo de uma requisição passa por URL routing, View, Serializer e Model antes de persistir no banco de dados.

### Frontend

O frontend utiliza arquitetura baseada em componentes com gerenciamento de estado centralizado via Vuex. Os componentes disparam actions que executam mutations no state, e as mudanças propagam reatividade para a interface. O Vue Router gerencia navegação client-side sem recarregar a página.

---

## Storage

O projeto utiliza um custom storage backend para integrar Django com Supabase Storage. Esta abordagem permite upload de imagens diretamente para CDN sem sobrecarregar o servidor de aplicação, resultando em melhor performance e menor custo de banda.

```python
# config/storage.py
class SupabaseStorage(Storage):
    """
    Custom Django storage backend for Supabase Storage.
    - Upload direto via API Supabase
    - URLs públicas via CDN (285+ edge locations)
    - Fallback para imagens legadas
    """
```

O Supabase Storage não aceita caracteres especiais em nomes de arquivo (acentos, cedilha). Todos os uploads utilizam apenas caracteres ASCII.

---

## CI/CD Pipeline

O projeto utiliza GitHub Actions para automação de integração contínua. O pipeline garante que todo código enviado ao repositório seja validado automaticamente através de linting e testes, mantendo a qualidade e consistência do codebase.

O workflow é acionado em pushes e pull requests para as branches `main` e `develop`. A estrutura separa verificações de backend e frontend em jobs independentes, permitindo execução paralela e feedback rápido.

| Job              | Descrição                              | Dependência   |
| ---------------- | -------------------------------------- | ------------- |
| `backend-lint`   | Verifica estilo e erros com Ruff       | -             |
| `backend-test`   | Executa testes com pytest e PostgreSQL | backend-lint  |
| `frontend-lint`  | Verifica código Vue.js com ESLint      | -             |
| `frontend-build` | Compila aplicação com Vite             | frontend-lint |

### Ferramentas de Qualidade

O backend utiliza Ruff como linter e formatter unificado, substituindo ferramentas como flake8, isort e black com melhor performance. Os testes rodam com pytest em um container PostgreSQL efêmero no CI.

| Ferramenta | Escopo   | Função                    |
| ---------- | -------- | ------------------------- |
| Ruff       | Backend  | Linter e formatter Python |
| Pytest     | Backend  | Framework de testes       |
| ESLint     | Frontend | Linter JavaScript/Vue     |
| Vite       | Frontend | Build e bundling          |

### Pre-commit Hooks

O projeto utiliza pre-commit para executar verificações automaticamente antes de cada commit. Para instalar os hooks localmente:

```bash
pip install pre-commit
pre-commit install
```

---

## Decisões Arquiteturais

As decisões abaixo foram tomadas considerando o contexto de projeto: um case para portfólio com foco em técnicas modernas, mantendo custo zero de infraestrutura.

| Decisão            | Justificativa                                   |
| ------------------ | ----------------------------------------------- |
| Monorepo           | Facilita desenvolvimento local e versionamento  |
| API REST           | Simples, stateless, amplamente suportado        |
| SPA                | UX fluida, separação clara de responsabilidades |
| PostgreSQL         | ACID compliance, JSON support, escalabilidade   |
| CDN para assets    | Performance global, offload do servidor         |
| Serviços separados | Cada componente otimizado para sua função       |
| Ruff over Black    | Ferramenta unificada, 10-100x mais rápida       |
| GitHub Actions     | CI/CD integrado ao repositório, gratuito        |

---

**Última revisão:** 30/01/2026
