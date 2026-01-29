# CHANGELOG

Todas as mudanças notáveis do projeto Terra Viva serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

---

## [0.4.0] - 2026-01-29

### Contexto

Reorganização completa da estrutura do projeto em monorepo, separando backend e frontend em diretórios dedicados. Atualização de toda a documentação técnica para padrão profissional.

### Adicionado

- Estrutura monorepo: `terraviva/backend` e `terraviva/frontend`
- `docs/DEPLOYMENT.md` com configuração de infraestrutura
- Prosa introdutória em todas as seções de documentação

### Modificado

- **Estrutura do Projeto**
  - `order/`, `product/` => `terraviva/backend/apps/`
  - `terraviva/` (config) => `terraviva/backend/config/`
  - `terraviva_v/` => `terraviva/frontend/`
  - `requirements.txt` => `terraviva/backend/requirements/base.txt`

- **Imports e Configurações**
  - Apps registrados como `apps.product`, `apps.order`
  - `DJANGO_SETTINGS_MODULE` atualizado para `config.settings`
  - Todos os imports internos atualizados

- **Documentação**
  - README.md com seções profissionais e prosa
  - ARCHITECTURE.md focado em estado atual
  - ROADMAP.md com fases detalhadas
  - ENVIRONMENT.md atualizado para nova estrutura

### Removido

- Arquivos Vue CLI obsoletos (`babel.config.js`, `vue.config.js`)
- Estrutura flat de diretórios na raiz

---

## [0.3.0] - 2026-01-29

### Contexto

Migração completa do build system de Vue CLI para Vite, eliminando todas as vulnerabilidades do frontend e atualizando o framework CSS Bulma para versão 1.0.

### Adicionado

- **Vite Build System**
  - `vite.config.js` com proxy para API em desenvolvimento
  - Suporte a `import.meta.env` para variáveis de ambiente
  - Hot Module Replacement (HMR) otimizado
  - Build de produção ~3s (vs ~30s com Vue CLI)

- **CI/CD Keep-Alive**
  - GitHub Actions workflow para ping diário do Supabase
  - Previne pausa automática por inatividade (7 dias)
  - Ping do Render para manter serviço ativo

### Modificado

- **Frontend Dependencies**
  - Vue CLI => Vite 6.4.1
  - Vue: 3.2.13 => 3.5.13
  - Vue Router: 4.0.11 => 4.5.0
  - Vuex: 4.0.2 => 4.1.0
  - Bulma: 0.9.4 => 1.0.2
  - Vulnerabilidades: 8 => 0

- **Build Configuration**
  - `index.html` movido para raiz do projeto (requisito Vite)
  - Imports com extensão `.vue` explícita
  - Variáveis de ambiente: `VUE_APP_*` => `VITE_*`

- **Estilos**
  - Correções para compatibilidade Bulma 1.0
  - Fix de cores em botões `.is-success` e `.is-outlined`
  - Fix de background em `.navbar-item` ativo
  - Logo header com `display: inline` (fix espaçamento)

- **Repositório**
  - Renomeado: `projeto-terraviva` => `terraviva-ecommerce-fullstack`

### Removido

- Vue CLI e plugins (`@vue/cli-service`, `@vue/cli-plugin-*`)
- `babel.config.js` (Vite usa esbuild)
- `vue.config.js` (substituído por `vite.config.js`)
- Dependências deprecated do Webpack

### Corrigido

- Espaçamento no logo "terraviva" no header
- Cores de botões e ícones para Bulma 1.0
- Router usando `import.meta.env.BASE_URL`

### Segurança

- **Frontend:** 0 vulnerabilidades (era 8 moderate)
- Todas as dependências atualizadas para versões seguras

### Infraestrutura

- **Build:** Vite 6.4.1 (substituiu Vue CLI 5.x)
- **Frontend:** Vercel com `VITE_API_URL` configurado
- **Repositório:** github.com/fabiodelllima/terraviva-ecommerce-fullstack

---

### Em Desenvolvimento

- Documentação BUSINESS_RULES.md
- Documentação DEPLOYMENT.md

---

## [2.1.0] - 2026-01-11

### Contexto

Implementação de armazenamento persistente de mídia via Supabase Storage, resolvendo o problema de arquivos efêmeros no Render.com. Inclui upgrade do Django para versão 5.2.10 devido a incompatibilidades com Python 3.14.

### Adicionado

- **Supabase Storage Integration**
  - Custom storage backend (`terraviva/storage.py`) para Supabase
  - Upload de imagens diretamente para bucket `media/uploads/`
  - URLs públicas via CDN Supabase (285 POPs globalmente)
  - Fallback gracioso para imagens legadas

- **Configuração de STORAGES**
  - Django 5.2+ STORAGES dict para gerenciamento de storage
  - WhiteNoise mantido para arquivos estáticos
  - Supabase para arquivos de mídia (uploads)

### Modificado

- **Django Upgrade**
  - Django: 4.2.17 => 5.2.10 (compatibilidade Python 3.14)
  - Correção do bug `AttributeError: 'super' object has no attribute 'dicts'`
  - Configuração migrada de `DEFAULT_FILE_STORAGE` para `STORAGES`

- **Product Model**
  - Método `make_thumbnail()` corrigido (path duplication fix)
  - Métodos `get_image()` e `get_thumbnail()` com error handling
  - `verbose_name_plural` corrigido para "Produtos"

- **Frontend Deploy**
  - Migração de Netlify para Vercel
  - Configuração `vercel.json` para SPA routing

- **Dependencies**
  - supabase: 2.27.1 (novo)
  - storage3: 2.27.1 (novo)
  - Pillow: 12.1.0 (mantido)

### Removido

- Campo `image_url` do model Product (redundante com Supabase URLs)
- Configuração `DEFAULT_FILE_STORAGE` (deprecated Django 5.2)
- Configuração `STATICFILES_STORAGE` duplicada
- `netlify.toml` (migrado para Vercel)
- `Procfile` (era para Heroku, não utilizado)

### Corrigido

- Incompatibilidade Python 3.14 + Django 4.2/5.1 (template context bug)
- Path duplication em thumbnails (`uploads/uploads/file.jpg`)
- Error handling para imagens legadas (404 no Supabase)

### Infraestrutura

- **Backend:** Render.com (<https://terraviva-api-bg8s.onrender.com\>\)
- **Frontend:** Vercel (<https://terraviva.vercel.app\>\)
- **Database:** Supabase PostgreSQL (500MB free tier)
- **Storage:** Supabase Storage (1GB free tier, CDN global)

---

## [2.0.1] - 2026-01-09

### Segurança

- **CRÍTICO:** SECRET_KEY removida do código-fonte e movida para variável de ambiente
- **CRÍTICO:** STRIPE_SECRET_KEY removida do código-fonte e movida para variável de ambiente
- DEBUG agora configurável via ambiente (evita DEBUG=True em produção)
- ALLOWED_HOSTS agora configurável via ambiente (evita host poisoning)
- Configurados security headers para produção (XSS, CSRF, SSL)

### Adicionado

- python-dotenv para gerenciamento de variáveis de ambiente
- .env.example como template de configuração
- docs/ENVIRONMENT.md com guia de configuração

### Modificado

- Pillow: 10.4.0 => 12.1.0 (compatibilidade Python 3.14)
- .gitignore atualizado para excluir arquivos .env

### Removido

- django-on-heroku (descontinuado)
- Secrets hardcoded do settings.py

---

## [2.0.0] - 2026-01-07

### Contexto

Início da **revitalização completa** do projeto após 4 anos sem manutenção (2022-2025). O objetivo é transformar o projeto acadêmico de 2021 em case para portfólio profissional de produção.

### Adicionado

- **Documentação Profissional Completa**
  - README.md reformulado com metodologia hierárquica
  - docs/ROADMAP.md com planejamento Fase 1, 2, 3
  - docs/ARCHITECTURE.md com análise estrutural
  - CHANGELOG.md seguindo Keep a Changelog format
  - LICENSE (MIT)
  - Estrutura docs/ criada

### Modificado

- **Backend Dependencies (Python)**
  - Python: 3.9 => 3.14
  - Django: 4.1.2 => 4.2.17 LTS
  - Pillow: 9.2.0 => 10.4.0
  - psycopg2-binary: 2.9.4 => 2.9.10
  - Django REST Framework: 3.14.0 => 3.15.2
  - djoser: 4.8.0 => 5.3.1
  - Stripe: 4.2.0 => 11.3.0

- **Frontend Dependencies (npm)**
  - Resolvidas 20 vulnerabilidades críticas/altas
  - Vulnerabilidades: 68 => 8 (todas moderate, dev-only)

### Segurança

- Resolvidas 20 de 28 vulnerabilidades npm (68 => 8)
- 8 vulnerabilidades restantes: moderate severity, dev-only

---

## [1.0.0] - 2021-12-XX

### Contexto

Release inicial do projeto acadêmico **Coding4Hope**. Plataforma e-commerce desenvolvida para automatizar vendas de uma ONG, substituindo processos manuais por sistema online completo.

### Adicionado

- **Backend Django**
  - Django 4.1.2 + Django REST Framework
  - Apps: `product`, `order`
  - Models: Product, Category, Order, OrderItem
  - API REST completa (CRUD produtos, checkout, auth)
  - Admin panel integrado
  - Integração Stripe (pagamentos)

- **Frontend Vue.js**
  - Vue.js 3.2.13 + Vue Router + Vuex
  - 10 páginas: Home, Product, Category, Search, Cart, Checkout, Success, Login, SignUp, MyAccount
  - Integração Stripe Elements
  - CSS framework: Bulma

### Impacto

Projeto entregue com sucesso à ONG, demonstrando viabilidade técnica e impacto social mensurável.

---

## Legenda

- `Adicionado`: Novas funcionalidades
- `Modificado`: Mudanças em funcionalidades existentes
- `Removido`: Funcionalidades removidas
- `Corrigido`: Correções de bugs
- `Segurança`: Correções de vulnerabilidades

---

**Última atualização:** 29/01/2026  
**Versão atual:** 0.4.0
