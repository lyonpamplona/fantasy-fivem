# Relatório de Auditoria Técnica

Escopo auditado:

- `backend-fantasy`
- `backend-heuristics`
- `frontend-game`
- `frontend-admin`
- `docker-compose.yaml`

## 1. Achados Críticos

### C1. Validação de JWT desabilitada no fluxo de usuário principal

Evidência:

- `backend-fantasy/routers/auth.py` usa `jwt.decode(..., options={"verify_signature": False})` em `get_current_user`.

Impacto:

- Permite forjar identidade de jogador sem chave válida, comprometendo integridade de inventário/saldo/mercado.

Recomendação:

- Validar assinatura obrigatoriamente com `JWT_SECRET`.
- Remover `verify_signature=False`.

### C2. Auto-criação de jogador com privilégios elevados no middleware de autenticação

Evidência:

- `backend-fantasy/routers/auth.py`: ao não encontrar jogador, cria automaticamente conta com `wallet_balance=1000000.0` e `is_vip=True`.

Impacto:

- Escalada econômica imediata e bypass de onboarding/controlos de criação.

Recomendação:

- Restringir comportamento a ambiente de desenvolvimento via feature flag explícita.
- Em produção, retornar `401/404` e exigir provisionamento controlado.

### C3. Segredo JWT e credenciais sensíveis hardcoded em `.env`

Evidência:

- `backend-fantasy/.env`, `backend-heuristics/.env`, `frontend-game/.env` contêm tokens/segredos reais em texto claro.

Impacto:

- Vazamento de segredo compromete autenticação e integrações externas.

Recomendação:

- Rotacionar segredos imediatamente.
- Manter apenas `.env.example` sem valores sensíveis.

## 2. Achados Altos

### H1. Inconsistência entre frontend admin e backend para ações críticas

Evidência:

- `frontend-admin/src/views/AdminDashboard.vue`: `toggleQuarantine` altera estado apenas no cliente, sem chamada à API.
- `confirmInjection` envia payload com `target_fivem_id` e `amount`.
- `backend-heuristics/routers/admin.py`: `inject_coins` ignora payload e injeta `+500000` para todos os jogadores.

Impacto:

- Ações aparentam executar no painel, mas comportamento real é diferente, com alto risco operacional.

Recomendação:

- Alinhar contrato de API e frontend.
- Exigir alvo e valor explícitos na API de injeção.

### H2. Autorização administrativa fraca

Evidência:

- `backend-heuristics/routers/admin.py`: login retorna token fixo `access_granted_admin`.
- Endpoints administrativos não exigem verificação de token.

Impacto:

- Qualquer cliente capaz de acessar endpoints pode operar ações administrativas.

Recomendação:

- Implementar JWT assinado com expiração curta.
- Proteger todos os endpoints admin com dependency de verificação.

### H3. Webhook sem validação de segredo

Evidência:

- `backend-heuristics/routers/webhook.py` não usa `WEBHOOK_SECRET`.

Impacto:

- Permite injeção de eventos falsos via requests não autenticados.

Recomendação:

- Validar assinatura/HMAC ou token compartilhado por header.

## 3. Achados Médios

### M1. Divergência de payload no webhook

Evidência:

- Schema declara `killer_id` (`schemas.py`), endpoint usa `shooter_id` (`routers/webhook.py`).

Impacto:

- Eventos podem ser descartados ou processados incorretamente.

Recomendação:

- Definir contrato único e validar com Pydantic.

### M2. Migrations com drift em relação aos modelos

Evidência:

- Migração `97dc...` remove `is_active` de `market_listings`, porém `models.py` mantém campo.
- Migração inicial define `cards.serial_number` como inteiro, modelo atual usa string.

Impacto:

- Erros em deploy/migração e inconsistência de schema.

Recomendação:

- Reconciliar cadeia Alembic com estado real do ORM.
- Criar migrações corretivas idempotentes.

### M3. Duplicidade de implementação de worker/event processing

Evidência:

- `backend-fantasy/tasks.py` e `backend-fantasy/worker.py` implementam `process_match_event`.
- Equivalente duplicado também existe em `backend-heuristics/worker.py`.

Impacto:

- Ambiguidade operacional e manutenção mais cara.

Recomendação:

- Consolidar em uma única implementação por serviço.

### M4. WebSocket não conectado ao canal Redis

Evidência:

- `routers/websocket.py` mantém conexões em memória, mas não assina `ws_card_updates`.

Impacto:

- Atualizações publicadas pelo worker não chegam automaticamente aos clientes conectados na API.

Recomendação:

- Implementar subscriber Redis na API ou gateway dedicado de realtime.

## 4. Achados Baixos

### L1. Duplicação estrutural entre `backend-fantasy` e `backend-heuristics`

Impacto:

- Maior custo de evolução, risco de divergência entre schemas e utilitários.

Recomendação:

- Extrair pacote compartilhado (modelos, auth, db base).

### L2. Sem suíte de testes automatizados no repositório

Impacto:

- Regressões passam sem detecção precoce.

Recomendação:

- Cobrir pelo menos smoke tests de endpoints críticos e contratos frontend/backend.

## 5. Pontos Positivos

- Separação de domínio entre gameplay e operação/admin.
- Estrutura de rotas organizada por contexto.
- Uso de Docker Compose simplifica execução local.
- Frontends com arquitetura Vue + Pinia consistente.

## 6. Prioridade de Correção Recomendada

1. Corrigir autenticação/autorização (C1, C2, H2, H3).
2. Corrigir contrato frontend-admin x backend-admin (H1, M1).
3. Resolver drift de migração (M2).
4. Consolidar pipeline de eventos assíncronos + websocket (M3, M4).
5. Introduzir testes e módulos compartilhados (L1, L2).
