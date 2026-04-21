# Fluxos e Módulos do Sistema

Este arquivo consolida os dois objetivos solicitados:

- mapeamento de todos os fluxos principais;
- descrição de todos os módulos relevantes.

## Fluxos Cobertos

1. Autenticação de jogador (dev login + bootstrap de sessão)
2. Compra de pack na loja oficial
3. Abertura de pack
4. Forja de cards
5. Contratos (staking)
6. Gestão de esquadrão
7. Mercado P2P (venda/compra/leilão/cancelamento)
8. Darkweb
9. Operação do painel admin
10. Ingestão de webhook de partida
11. Processamento assíncrono realtime por Celery
12. Auditoria noturna por Celery Beat (z-score)

Detalhamento completo: [system-flows.md](./system-flows.md)

## Módulos Cobertos

### Backend

- `backend-fantasy`: auth, cards, packs, market, user, squad, websocket, tasks.
- `backend-heuristics`: admin, webhook, worker realtime e tasks agendadas.

### Frontend

- `frontend-game`: login, deck, market, squad, stores e componentes.
- `frontend-admin`: login, dashboard e ações operacionais.

### Infra

- `docker-compose.yaml`, PostgreSQL, Redis, workers.

Detalhamento completo: [modules.md](./modules.md)

## Referências Cruzadas

- Arquitetura geral: [architecture.md](./architecture.md)
- Código completo (estrutura/config/deps): [codigo-completo.md](./codigo-completo.md)
- Endpoints por serviço: [api-map.md](./api-map.md)
- Riscos/achados da auditoria: [audit-report.md](./audit-report.md)
