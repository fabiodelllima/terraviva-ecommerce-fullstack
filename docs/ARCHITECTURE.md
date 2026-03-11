# ARCHITECTURE

**Versão:** 0.7.0

---

## Visão Geral

Terra Viva segue uma arquitetura de aplicação distribuída com separação completa entre frontend e backend. O frontend é uma Single Page Application (SPA) que consome uma API REST. O backend é stateless, permitindo escalabilidade horizontal.

A partir da versão 0.7.0, o backend adota princípios de Clean Architecture com separação em camadas bem definidas: Presentation, Application, Domain e Infrastructure. Esta estrutura facilita testabilidade, manutenção e evolução independente de cada camada.

A escolha por serviços cloud separados (Vercel, Render, Supabase) reflete uma arquitetura moderna onde cada componente é otimizado para sua função específica, em contraste com o modelo monolítico tradicional.

---

## Diagrama de Infraestrutura

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

## Clean Architecture

O backend implementa Clean Architecture adaptada ao contexto Django, organizando o código em camadas com dependências unidirecionais (de fora para dentro). Cada camada tem responsabilidade única e pode ser testada isoladamente.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  views.py - Controllers HTTP (thin, delegam para services)  │
│  serializers.py - DTOs para request/response                │
├─────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                        │
│  services.py - Orquestração de business logic               │
│  selectors.py - Queries de leitura (CQRS-lite)              │
├─────────────────────────────────────────────────────────────┤
│                      DOMAIN LAYER                           │
│  models.py - Entidades (dados e comportamento mínimo)       │
│  exceptions.py - Exceções de domínio                        │
│  validators.py - Regras de validação de negócio             │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE LAYER                      │
│  gateways/ - Integrações externas (Stripe, APIs)            │
│  storage.py - Backend de armazenamento (Supabase)           │
└─────────────────────────────────────────────────────────────┘
```

### Estrutura de Diretórios

```
terraviva/backend/
├── apps/
│   ├── order/
│   │   ├── exceptions.py      # PaymentError, InvalidOrderError
│   │   ├── gateways/
│   │   │   └── stripe.py      # StripeGateway
│   │   ├── models.py          # Order, OrderItem
│   │   ├── serializers.py     # OrderSerializer, MyOrderSerializer
│   │   ├── services.py        # OrderService
│   │   ├── validators.py      # validate_amount, validate_order_items
│   │   └── views.py           # checkout, OrdersList
│   └── product/
│       ├── models.py          # Category, Product
│       ├── selectors.py       # get_latest_products, search_products
│       ├── serializers.py     # ProductSerializer, CategorySerializer
│       ├── services.py        # ImageService
│       └── views.py           # LatestProductsList, ProductSearch
└── config/
    ├── settings.py
    ├── storage.py             # SupabaseStorage
    └── urls.py
```

---

## SOLID Principles

O código segue os princípios SOLID para garantir manutenibilidade e extensibilidade.

### Single Responsibility (SRP)

Cada classe tem uma única razão para mudar. Services orquestram lógica de negócio, Gateways encapsulam integrações externas, Validators validam regras específicas.

| Classe            | Responsabilidade única                        |
| ----------------- | --------------------------------------------- |
| `OrderService`    | Orquestração de criação e checkout de pedidos |
| `ImageService`    | Processamento e manipulação de imagens        |
| `StripeGateway`   | Comunicação com API do Stripe                 |
| `validate_amount` | Validação de valores monetários               |

### Open/Closed (OCP)

Gateways podem ser estendidos (novo gateway de pagamento) sem modificar Services existentes.

### Dependency Inversion (DIP)

Services recebem dependências via construtor, permitindo injeção de mocks para testes.

```python
class OrderService:
    def __init__(self, payment_gateway: StripeGateway | None = None) -> None:
        self.payment_gateway = payment_gateway or StripeGateway()
```

---

## Service Layer

Services contêm a lógica de negócio da aplicação, coordenando entre entidades, validators e gateways. São stateless e podem ser injetados com dependências.

### OrderService

Responsável pelo fluxo de checkout: cálculo de total, processamento de pagamento e criação de pedido.

```python
class OrderService:
    def calculate_total(self, items: list[dict]) -> Decimal
    def create_order(self, user: User, order_data: dict, items_data: list) -> Order
    def process_checkout(self, user: User, validated_data: dict) -> Order
```

### ImageService

Responsável por processamento de imagens, extraindo lógica que antes residia nos models.

```python
class ImageService:
    def make_thumbnail(cls, image, size, quality) -> File
    def get_safe_url(field) -> str
```

---

## Infrastructure Layer

### Gateways

Gateways encapsulam integrações com serviços externos, isolando o domínio de detalhes de implementação.

```python
class StripeGateway:
    def charge(self, amount: Decimal, token: str, description: str) -> str
```

O gateway implementa logging estruturado e tratamento de exceções específicas, convertendo erros do Stripe para exceções de domínio (`PaymentError`).

### Storage

O projeto utiliza um custom storage backend para integrar Django com Supabase Storage. Esta abordagem permite upload de imagens diretamente para CDN sem sobrecarregar o servidor de aplicação.

```python
class SupabaseStorage(Storage):
    def _save(self, name: str, content: File) -> str
    def url(self, name: str | None) -> str
```

---

## Domain Layer

### Exceptions

Exceções de domínio centralizam tratamento de erros, permitindo que a camada de apresentação retorne respostas HTTP apropriadas.

```python
class OrderException(Exception):
    """Base exception for order domain."""

class PaymentError(OrderException):
    """Raised when payment processing fails."""

class InvalidOrderError(OrderException):
    """Raised when order data is invalid."""
```

### Validators

Validators implementam programação defensiva com guard clauses, falhando rapidamente quando dados são inválidos.

```python
def validate_amount(amount: Decimal | None) -> None
def validate_payment_token(token: str | None) -> None
def validate_order_items(items: list[dict] | None) -> None
```

---

## Stack Tecnológico

| Camada   | Tecnologia            | Versão | Justificativa                        |
| -------- | --------------------- | ------ | ------------------------------------ |
| Runtime  | Python                | 3.13+  | Versão LTS, type hints avançados     |
| Backend  | Django                | 6.0    | Framework maduro, batteries included |
| API      | Django REST Framework | 3.15   | Padrão de facto para APIs Django     |
| Auth     | djoser                | 2.3    | Endpoints de auth prontos            |
| Payments | Stripe                | 11.3   | Líder de mercado em pagamentos       |
| Frontend | Vue.js                | 3.5    | Reativo, progressivo, curva suave    |
| Build    | Vite                  | 6.x    | Build rápido, HMR instantâneo        |
| State    | Vuex                  | 4.1    | Gerenciamento de estado centralizado |
| CSS      | Bulma                 | 1.0    | CSS-only, sem JS, customizável       |

---

## Ferramentas de Qualidade

O projeto utiliza ferramentas modernas para garantir qualidade de código e type safety.

| Ferramenta | Função                                 | Configuração              |
| ---------- | -------------------------------------- | ------------------------- |
| Ruff       | Linter e formatter Python              | `pyproject.toml`          |
| Pyright    | Type checker (mesmo engine do Pylance) | `pyproject.toml`          |
| Mypy       | Type checker com plugin Django         | `pyproject.toml`          |
| Pytest     | Framework de testes                    | `pyproject.toml`          |
| ESLint     | Linter JavaScript/Vue                  | `.eslintrc.js`            |
| Prettier   | Formatter frontend                     | `.prettierrc`             |
| Pre-commit | Hooks de validação                     | `.pre-commit-config.yaml` |

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

O pipeline executa: trailing-whitespace, end-of-file-fixer, check-yaml, ruff, pyright, eslint, prettier.

---

## CI/CD Pipeline

O projeto utiliza GitHub Actions para automação de integração contínua. O workflow é acionado em pushes e pull requests para as branches `main` e `develop`.

| Job              | Descrição                              | Dependência   |
| ---------------- | -------------------------------------- | ------------- |
| `backend-lint`   | Verifica estilo e tipos com Ruff       | -             |
| `backend-test`   | Executa testes com pytest e PostgreSQL | backend-lint  |
| `frontend-lint`  | Verifica código Vue.js com ESLint      | -             |
| `frontend-build` | Compila aplicação com Vite             | frontend-lint |

---

## Decisões Arquiteturais

| Decisão               | Justificativa                                          |
| --------------------- | ------------------------------------------------------ |
| Clean Architecture    | Separação de concerns, testabilidade, manutenibilidade |
| Service Layer         | Lógica de negócio isolada de frameworks                |
| Gateway Pattern       | Integrações externas facilmente mockáveis              |
| Domain Exceptions     | Tratamento de erros consistente                        |
| Defensive Programming | Fail-fast com validators e guard clauses               |
| Monorepo              | Facilita desenvolvimento local e versionamento         |
| API REST              | Simples, stateless, amplamente suportado               |
| SPA                   | UX fluida, separação clara de responsabilidades        |

---

**Última revisão:** 11/03/2026
