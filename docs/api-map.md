# Mapa de APIs

## 1. Backend Fantasy (`:8000`)

### Health

- `GET /health/live` - liveness do serviço.

### Auth (`/api/auth`)

- `GET /dev-login/{steam_id}` - login dev e geração de token.

### User (`/api/user`)

- `GET /me/profile` - perfil do jogador autenticado.

### Cards (`/api/cards`)

- `GET /user/me` - lista cards do jogador.
- `POST /forge` - forja de 5 cards em 1 novo.
- `POST /{card_id}/contract` - assinatura de contrato.

### Packs (`/api/packs`)

- `GET /user/me` - packs do jogador.
- `POST /open/{pack_type}` - abertura de pack.

### Market (`/api/market`)

- `GET /store` - tabela de preços dinâmicos de packs.
- `POST /buy/{pack_type}` - compra de pack da loja oficial.
- `GET /p2p` - listagem ativa de anúncios.
- `GET /p2p/history/{card_id}` - histórico sintético de preço.
- `POST /p2p/sell/{card_id}` - criar anúncio.
- `POST /p2p/buy/{listing_id}` - comprar anúncio direto.
- `POST /p2p/bid/{listing_id}` - lance em leilão.
- `DELETE /p2p/cancel/{listing_id}` - cancelar anúncio.
- `GET /darkweb/status` - status da janela darkweb.
- `POST /darkweb/buy` - compra de pack classificado.

### Squad (`/api/squad`)

- `GET /` - cards alocados no esquadrão.
- `POST /deploy/{card_id}` - alocação por slot/role.
- `POST /remove/{card_id}` - remoção do slot.

### WebSocket

- `WS /ws/feed` - endpoint websocket registrado na API.

## 2. Backend Heuristics (`:8001`)

### Health

- `GET /health/live` - liveness do serviço.

### Admin (`/api/admin`)

- `POST /login` - autenticação administrativa.
- `GET /suspects` - top suspeitos com agregados.
- `POST /toggle_quarantine/{player_id}` - alterna quarentena do jogador.
- `GET /player/{player_id}/dossier` - relatório de dossiê.
- `POST /seed_mocks` - gera dados mockados.
- `DELETE /clear_mocks` - remove dados mockados.
- `POST /inject_coins` - injeta saldo em massa.

### Webhook (`/api/webhook`)

- `POST /match_event` - ingestão de evento de partida.

## 3. Autenticação e Headers

### Jogo

- Front envia `Authorization: Bearer <token>` para rotas protegidas.

### Admin

- Front armazena `admin_token` em `localStorage`.
- Rotas de dashboard não enviam token no request atualmente.

## 4. Respostas e códigos

- A maioria das rotas usa JSON simples com `status`, `detail`, ou payload de entidade.
- Erros de negócio são retornados via `HTTPException` (400/401/403/404).
