# Arquitetura Técnica

## 1. Visão Geral

A solução usa arquitetura distribuída por domínio:

- Domínio de gameplay/economia no `backend-fantasy`.
- Domínio de observabilidade/moderação no `backend-heuristics`.
- Duas interfaces web independentes (jogo e admin).
- Infra de suporte compartilhada (PostgreSQL e Redis).

## 2. Componentes

### 2.1 `backend-fantasy`

Responsável por:

- autenticação de jogador (modo dev);
- inventário de cards;
- abertura de packs;
- forja de cards;
- gestão de esquadrão;
- mercado oficial e P2P;
- status de darkweb.

Entradas principais:

- APIs REST em `/api/auth`, `/api/cards`, `/api/packs`, `/api/market`, `/api/user`, `/api/squad`.

Dependências:

- PostgreSQL (leitura/escrita de entidades de jogo);
- Redis (broker/backend Celery e publicação de eventos).

### 2.2 `worker-fantasy` (Celery)

Responsável por processamento assíncrono do evento `process_match_event`.

- Atualiza score/sinais de jogador e evolução de cards.
- Publica atualizações em canal Redis `ws_card_updates`.

### 2.3 `backend-heuristics`

Responsável por:

- login admin;
- ranking/lista de suspeitos;
- dossiê de jogador;
- geração/limpeza de mocks;
- webhook de partida.

Entradas principais:

- APIs REST em `/api/admin` e `/api/webhook`.

### 2.4 `frontend-game`

Cliente Vue para jogadores:

- login dev;
- deck/arsenal;
- abertura de packs e forja;
- mercado (store/P2P/darkweb);
- esquadrão e sinergia.

### 2.5 `frontend-admin`

Cliente Vue para operação:

- autenticação administrativa;
- visualização de suspeitos;
- ações operacionais (mocks, bloqueio, injeção de coins, dossiê).

## 3. Modelo de Dados

As duas APIs compartilham o mesmo esquema lógico (tabelas principais):

- `players`
- `cards`
- `market_listings`
- `player_packs`
- `admin_logs`
- `market_history`
- `buy_orders`

Observação: as duas aplicações importam modelos muito similares, apontando para o mesmo banco.

## 4. Comunicação Entre Camadas

### 4.1 Frontend -> Backend

- `frontend-game` consome `backend-fantasy` via `VITE_API_URL`.
- `frontend-admin` consome `backend-heuristics` via `VITE_API_URL`.

### 4.2 Backend -> Banco

- SQLAlchemy assíncrono para APIs FastAPI.
- Sessão síncrona em tarefas Celery (`tasks.py`) no `backend-fantasy`.

### 4.3 Backend -> Mensageria

- `backend-fantasy` + worker usam Redis para broker/result backend.

## 5. Deploy Local (Docker Compose)

Serviços definidos:

- `db` (PostgreSQL)
- `redis`
- `api-fantasy`
- `worker-fantasy`
- `api-heuristics`
- `frontend-game`
- `frontend-admin`

## 6. Configuração (variáveis)

### `backend-fantasy/.env`

- `DATABASE_URL`
- `DATABASE_URL_SYNC`
- `REDIS_URL`
- `JWT_SECRET`
- `FRONTEND_GAME_URL`

### `backend-heuristics/.env`

- `DATABASE_URL`
- `ADMIN_PASSWORD`
- `WEBHOOK_SECRET`
- `FRONTEND_ADMIN_URL`

### Frontends

- `frontend-game/.env`: `VITE_API_URL`, branding.
- `frontend-admin/.env`: `VITE_API_URL`, branding.

## 7. Pontos Arquiteturais Relevantes

- Backend de gameplay e backend admin compartilham banco e modelos equivalentes.
- Existe implementação assíncrona e síncrona de processamento de evento em arquivos distintos (`worker.py` e `tasks.py`), com sobreposição funcional.
- Existe rota websocket (`/ws/feed`) sem subscriber Redis ativo no processo da API.

Ver análise de impacto em [Relatório de Auditoria](./audit-report.md).
