"""Auxiliares de integracao externa para alertas de moderacao."""

import os

import httpx

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_ADMIN_WEBHOOK")
FIVEM_SERVER_API_URL = os.getenv("FIVEM_SERVER_API_URL")
FIVEM_API_KEY = os.getenv("FIVEM_API_KEY")

def alert_server_moderation(fivem_id: str, nickname: str, reason: str):
    """Notifica o Discord e o endpoint opcional de moderacao do FiveM.

    Falhas sao propositalmente ignoradas para nao interromper o fluxo de webhook.
    """
    try:
        discord_payload = {
            "content": f"🚨 **ALERTA DO FANTASY GAME** 🚨\n**Jogador:** {nickname} (ID: {fivem_id})\n**Motivo:** {reason}\n**Ação:** Status alterado para MONITORED."
        }
        httpx.post(DISCORD_WEBHOOK_URL, json=discord_payload, timeout=5.0)

        if FIVEM_SERVER_API_URL:
            fivem_payload = {
                "action": "flag_suspect",
                "target_id": fivem_id,
                "reason": reason
            }
            headers = {"Authorization": f"Bearer {FIVEM_API_KEY}"}
            httpx.post(FIVEM_SERVER_API_URL, json=fivem_payload, headers=headers, timeout=5.0)
            
    except Exception:
        pass
