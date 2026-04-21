# Visão Geral do Código

Este documento descreve o código como um todo: estrutura, responsabilidades de cada parte, funções-chave, configuração e dependências.

## 1. Objetivo do Projeto

A plataforma combina dois domínios:

- **Fantasy (gameplay/economia):** inventário de cartas, packs, forja, mercado e esquadrão.
- **Heurística (segurança/moderação):** avaliação de comportamento, painel admin, ingestão de eventos e auditoria estatística.

## 2. Estrutura do Repositório

```text
.
├── backend-fantasy/      # API gameplay + tasks de XP
├── backend-heuristics/   # API admin + heurística realtime e noturna
├── frontend-game/        # SPA de jogador (Vue)
├── frontend-admin/       # SPA de operador/admin (Vue)
├── docs/                 # documentação técnica
└── docker-compose.yaml   # orquestração local
```

## 3. Backend Fantasy

### 3.1 Função principal

- Expor APIs REST para o jogo.
- Persistir estado econômico e de progressão.
- Consumir task assíncrona de XP (`fantasy.process_xp`).

### 3.2 Arquivos centrais

- `main.py`: inicialização FastAPI, CORS e rotas.
- `models.py`: entidades de domínio (Player, Card, MarketListing, etc.).
- `routers/*.py`: endpoints de auth/cards/packs/market/squad/users/ws.
- `celery_app.py`: configuração Celery do domínio fantasy.
- `tasks.py`: task que processa XP e publica atualizações em Redis.

## 4. Backend Heuristics

### 4.1 Função principal

- Expor painel admin (`/api/admin`) e webhook de partida (`/api/webhook`).
- Processar heurísticas em tempo real (`worker.py`).
- Executar auditoria estatística agendada (`tasks.py`, z-score).

### 4.2 Arquivos centrais

- `main.py`: inicialização da API admin.
- `routers/admin.py`: login admin, suspects, dossiê, ações operacionais.
- `routers/webhook.py`: entrada de evento de match.
- `worker.py`: regras anti-cheat realtime + encaminhamento para `fantasy.process_xp`.
- `celery_app.py`: configuração Celery + agenda (`beat_schedule`).
- `tasks.py`: análise global noturna por desvio padrão/z-score.
- `models.py`: modelos compartilhados e modelos específicos de heurística (`PlayerStats`, `FinancialLog`).

## 5. Frontends

### 5.1 `frontend-game`

- Autenticação de jogador (dev).
- Gestão de deck, packs, forja e squad.
- Mercado oficial, P2P e darkweb.

### 5.2 `frontend-admin`

- Login operacional.
- Painel de suspeitos e dossiê.
- Ações administrativas de simulação/operação.

## 6. Fluxo Assíncrono (Resumo)

1. Evento de partida entra no domínio de heurística.
2. `backend-heuristics/worker.py` calcula suspeita, aplica anti-abuso e pode alertar Discord.
3. Worker envia task `fantasy.process_xp`.
4. `backend-fantasy/tasks.py` atualiza XP/kills/cards e publica `ws_card_updates` no Redis.
5. Em paralelo, `backend-heuristics/tasks.py` executa análise noturna por z-score (Celery Beat).

## 7. Configuração e Execução

## 7.1 Via Docker (recomendado)

```bash
docker compose up --build
```

Serviços expostos:

- API Fantasy: `http://localhost:8000`
- API Heuristics: `http://localhost:8001`
- Front Game: `http://localhost:5173`
- Front Admin: `http://localhost:5174`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

Observacao:

- No `docker-compose.yaml` atual existe `worker-fantasy`.
- `worker`/`beat` de heuristica podem ser iniciados manualmente pelos comandos da secao 9.

## 7.2 Variáveis de ambiente

- `backend-fantasy/.env`: DB, Redis, JWT, CORS game.
- `backend-heuristics/.env`: DB, Redis, senha admin, webhook secret.
- `frontend-game/.env`: URL da API de jogo.
- `frontend-admin/.env`: URL da API admin.

## 7.3 Dependências de sistema

- Docker + Docker Compose.
- (Sem Docker) Python 3.11, Node 18/20, PostgreSQL 15, Redis 7.

## 8. Dependências por aplicação

### Backends (pip)

Principais bibliotecas:

- `fastapi`, `uvicorn`
- `sqlalchemy`, `asyncpg`, `psycopg2-binary`
- `celery`, `redis`
- `pyjwt`, `python-dotenv`
- `httpx` (e `aiohttp` no domínio heurístico para webhook de alerta)

### Frontends (npm)

- `vue`, `pinia`, `vue-router`
- `vite`
- `tailwindcss`, `postcss`, `autoprefixer`

## 9. Comandos úteis para manutenção

```bash
# Validar sintaxe Python
python3 -m compileall backend-fantasy backend-heuristics

# Subir apenas API Fantasy localmente
cd backend-fantasy && uvicorn main:app --reload --port 8000

# Subir worker fantasy
cd backend-fantasy && celery -A celery_app:celery_app worker --loglevel=info

# Subir worker heuristics
cd backend-heuristics && celery -A celery_app:celery_app worker --loglevel=info

# Subir beat heuristics (tarefas noturnas)
cd backend-heuristics && celery -A celery_app:celery_app beat --loglevel=info
```
