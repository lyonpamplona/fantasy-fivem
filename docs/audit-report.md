# Relatório de Auditoria Técnica

Escopo auditado:

- `backend-fantasy`
- `backend-heuristics`
- `frontend-game`
- `frontend-admin`
- `docker-compose.yaml`

## 1. Achados Críticos

### C1. Validação de assinatura JWT desabilitada no fluxo principal de jogador

Evidência:

- `backend-fantasy/routers/auth.py`: `jwt.decode(..., options={"verify_signature": False})`.

Impacto:

- Permite falsificação de identidade (`sub`) e acesso indevido aos recursos do jogador.

Recomendação:

- Remover `verify_signature=False` e validar assinatura com `JWT_SECRET`.

### C2. Auto-provisionamento de conta com saldo e VIP elevados

Evidência:

- `backend-fantasy/routers/auth.py`: criação automática de jogador com `wallet_balance=1000000.0` e `is_vip=True`.

Impacto:

- Quebra de integridade econômica e bypass de onboarding/autorização.

Recomendação:

- Restringir estritamente a ambiente de desenvolvimento via flag de feature.

## 2. Achados Altos

### H1. Autenticação/Autorização administrativa fraca

Evidência:

- `backend-heuristics/routers/admin.py`: login retorna token fixo (`access_granted_admin`).
- Endpoints administrativos não exigem validação explícita desse token.

Impacto:

- Alto risco de uso indevido das ações administrativas.

Recomendação:

- Implementar JWT assinado com expiração e dependency de autorização nos endpoints admin.

### H2. Divergência entre frontend-admin e ações reais da API

Evidência:

- Painel envia payload de injeção por alvo/valor, mas API atual executa incremento em massa (`+500000`) para todas as contas.

Impacto:

- Comportamento operacional diferente da intenção do operador.

Recomendação:

- Definir contrato explícito (target + amount) e alinhar frontend/backend.

## 3. Achados Médios

### M1. Dependência ausente para pipeline heurístico

Evidência:

- `backend-heuristics/tasks.py` e `backend-heuristics/worker.py` usam `aiohttp`.
- `backend-heuristics/requirements.txt` não declara `aiohttp`.

Impacto:

- Falha de runtime em worker/tarefas (`ModuleNotFoundError`).

Recomendação:

- Adicionar `aiohttp` ao `requirements.txt` do domínio heurístico.

### M2. Modelo de dados compartilhado entre domínios com alto acoplamento

Evidência:

- `backend-heuristics/models.py` inclui entidades de gameplay e de heurística no mesmo conjunto.

Impacto:

- Evolução e migração mais arriscadas entre contextos de negócio diferentes.

Recomendação:

- Separar bounded contexts (ou aplicar estratégia clara de ownership por tabela).

### M3. Fluxos assíncronos relevantes não estão totalmente representados no compose

Evidência:

- Código possui worker/beat heurístico (`backend-heuristics/celery_app.py`, `tasks.py`, `worker.py`).
- `docker-compose.yaml` atual sobe apenas `worker-fantasy`.

Impacto:

- Funcionalidades de auditoria noturna/realtime podem não estar ativas por padrão.

Recomendação:

- Adicionar serviços de worker/beat heurístico no compose ou documentar execução obrigatória manual.

## 4. Achados Baixos

### L1. Inconsistências de naming e payload entre componentes

Evidência:

- Variações de campos de evento (ex.: shooter/killer) em partes distintas do sistema.

Impacto:

- Aumenta chance de integração quebrada ao evoluir webhooks e workers.

Recomendação:

- Consolidar contrato de evento e centralizar schema canônico.

## 5. Pontos Positivos

- Arquitetura separada entre experiência de jogo e operação admin.
- Pipeline assíncrono com Celery/Redis já estruturado para escalar processamento.
- Frontends separados por persona (jogador vs operador).
- Documentação técnica abrangente em `docs/`.

## 6. Prioridade Recomendada de Correção

1. Segurança de autenticação (C1, C2, H1).
2. Contrato operacional admin (H2).
3. Estabilidade de runtime e deploy assíncrono (M1, M3).
4. Redução de acoplamento de modelos e padronização de payload (M2, L1).
