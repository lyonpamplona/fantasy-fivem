# Mapa de Módulos

## 1. Backend Fantasy (`backend-fantasy`)

### Núcleo

- `main.py`: bootstrap FastAPI, CORS, healthcheck e registro de routers.
- `database.py`: engine assíncrona, session factory e dependency `get_db`.
- `models.py`: entidades ORM (Player, Card, MarketListing, etc.).
- `auth.py`: emissão e validação de JWT (usuário/admin).
- `schemas.py`: schema `WebhookPayload`.

### Assíncrono e integração

- `celery_app.py`: instancia app Celery com Redis.
- `tasks.py`: task `process_match_event` (versão síncrona com SQLAlchemy sync).
- `worker.py`: versão alternativa de processamento (async + publish Redis).
- `utils.py`: integração externa para alerta/moderação (Discord/FiveM API).

### Rotas de domínio

- `routers/auth.py`: login dev + resolução de usuário atual.
- `routers/users.py`: perfil do jogador autenticado.
- `routers/cards.py`: inventário, forja e contratos.
- `routers/packs.py`: inventário e abertura de packs.
- `routers/market.py`: loja oficial, P2P, leilão e darkweb.
- `routers/squad.py`: deploy/remoção e consulta de esquadrão.
- `routers/websocket.py`: endpoint websocket e broadcast em memória.

### Dados/migração

- `alembic/`: migrações de banco.
- `init_db.py`: criação de tabelas via metadata.
- `setup_test.py`: seed básico e emissão de token de teste.

## 2. Backend Heuristics (`backend-heuristics`)

### Núcleo

- `main.py`: bootstrap FastAPI e CORS do painel admin.
- `database.py`: engine/session assíncras para admin service.
- `models.py`: modelos equivalentes ao serviço fantasy.
- `auth.py`: helpers JWT.
- `schemas.py`: schema de payload de evento.

### Rotas

- `routers/admin.py`: login, lista de suspeitos, dossiê e operações administrativas.
- `routers/webhook.py`: ingestão de evento de partida para score de suspeita.

### Suporte

- `utils.py`: alerta de moderação externo.
- `worker.py`: processamento assíncrono alternativo de evento.
- `alembic/`, `init_db.py`, `setup_test.py`: infraestrutura de dados.

## 3. Frontend Game (`frontend-game`)

### Base

- `src/main.js`, `src/App.vue`: inicialização da SPA e shell visual.
- `src/router/index.js`: rotas e guard de autenticação.
- `src/stores/fantasy.js`: estado global de perfil/cards/packs.
- `src/stores/toast.js`: notificações de UI.

### Vistas

- `src/views/Login.vue`: login dev.
- `src/views/Deck.vue`: inventário, abertura e forja.
- `src/views/Market.vue`: loja, P2P e darkweb.
- `src/views/Squad.vue`: alocação e sinergia tática.

### Componentes

- `src/components/FantasyCard.vue`: card visual e animações.
- `src/components/CardDetailsModal.vue`: detalhes + ações de mercado/contrato.
- `src/components/ToastNotification.vue`: toasts.

## 4. Frontend Admin (`frontend-admin`)

### Base

- `src/main.js`, `src/App.vue`: shell da SPA admin.
- `src/router/index.js`: rotas protegidas por token local.
- `src/stores/toast.js`: notificações.

### Vistas

- `src/views/AdminLogin.vue`: autenticação de operador.
- `src/views/AdminDashboard.vue`: monitoramento, ações e dossiê.

### Componentes

- `src/components/ToastNotification.vue`: toasts do painel.

## 5. Infra (`docker-compose.yaml`)

Define orquestração local de todos os serviços, volumes persistentes e portas públicas.
