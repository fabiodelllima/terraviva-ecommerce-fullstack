# DEPLOYMENT

**Versão:** 0.4.0

---

## Visão Geral

O projeto está deployado em três serviços cloud gratuitos, cada um especializado em sua função. Esta arquitetura distribuída permite escalabilidade independente de cada camada e aproveita os free tiers para manter custo zero de operação.

| Serviço  | Função     | URL                                        |
| -------- | ---------- | ------------------------------------------ |
| Vercel   | Frontend   | https://terraviva.vercel.app               |
| Render   | Backend    | https://terraviva-api-bg8s.onrender.com    |
| Supabase | DB/Storage | (conexão interna)                          |

---

## Render (Backend)

O backend Django roda em container gerenciado no Render. O serviço está configurado para auto-deploy a partir da branch main, com build automático das dependências Python. O gunicorn serve a aplicação WSGI em produção.

| Configuração   | Valor                                  |
| -------------- | -------------------------------------- |
| Service Type   | Web Service                            |
| Root Directory | `terraviva/backend`                    |
| Build Command  | `pip install -r requirements/base.txt` |
| Start Command  | `gunicorn config.wsgi:application`     |
| Auto-Deploy    | `main` branch                          |

O free tier do Render suspende o serviço após 15 minutos de inatividade. O primeiro request após suspensão leva aproximadamente 30 segundos (cold start).

---

## Vercel (Frontend)

O frontend Vue.js é servido pela Vercel como site estático com CDN global. O Vite gera o bundle de produção otimizado, e a Vercel distribui os assets através de edge locations mundiais. Preview deployments são gerados automaticamente para cada pull request.

| Configuração     | Valor                |
| ---------------- | -------------------- |
| Framework        | Vite                 |
| Root Directory   | `terraviva/frontend` |
| Build Command    | `npm run build`      |
| Output Directory | `dist`               |
| Auto-Deploy      | `main` branch        |

A variável de ambiente `VITE_API_URL` aponta para a API no Render, permitindo que o frontend faça requisições cross-origin autenticadas via CORS.

---

## Supabase

O Supabase fornece PostgreSQL gerenciado e storage de arquivos com CDN integrado. A conexão com o banco é feita via connection string no formato `DATABASE_URL`, e o storage utiliza um custom backend Django para uploads.

O banco PostgreSQL oferece 500MB no free tier, suficiente para o volume de dados do projeto. O storage disponibiliza 1GB com distribuição via 285+ edge locations globalmente.

---

## GitHub Actions

Um workflow de keep-alive executa ping na API a cada 14 minutos para evitar suspensão automática do Render. Este workaround é necessário apenas no free tier e pode ser removido em planos pagos.

---

**Última revisão:** 29/01/2026
