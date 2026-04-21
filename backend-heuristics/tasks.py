"""Tarefas assíncronas de auditoria estatística (z-score global).

Executa varredura periodica para identificar contas com comportamento
fora da distribuicao normal do servidor.
"""

import asyncio
import math
import os

import aiohttp
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from celery_app import celery_app
from database import AsyncSessionLocal
from models import PlayerStats

async def send_discord_alert(player_id, nickname, score, reason):
    """Envia alerta para webhook Discord com contexto da anomalia."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return
    
    content = f"🚨 **AUDITORIA NOTURNA (Z-SCORE)** 🚨\n**Alvo:** `{nickname}` (ID: {player_id})\n**Taxa de HS:** {score}\n**Gatilho:** {reason}\n**Ação:** Conta suspensa preventivamente."
    payload = {"content": content}
    
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)

async def async_run_z_score():
    """Executa analise estatistica de HS-rate e marca contas monitoradas."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(PlayerStats).options(selectinload(PlayerStats.player)).where(PlayerStats.kills >= 100)
        )
        stats = result.scalars().all()

        if len(stats) < 5:
            return

        hs_rates = [s.headshots / s.kills for s in stats if s.kills > 0]
        if not hs_rates:
            return

        avg_hs = sum(hs_rates) / len(hs_rates)
        variance = sum((r - avg_hs) ** 2 for r in hs_rates) / len(hs_rates)
        std_dev = math.sqrt(variance)

        threshold = avg_hs + (std_dev * 3)
        if threshold < 0.60:
            threshold = 0.60

        for s in stats:
            if s.kills == 0:
                continue
            rate = s.headshots / s.kills
            if rate >= threshold or rate >= 0.85:
                if not s.player.is_monitored:
                    s.player.is_monitored = True
                    s.player.suspicion_score = max(s.player.suspicion_score, 85.0)
                    
                    rate_str = f"{(rate*100):.1f}%"
                    reason_str = f"Desvio Padrão Extremo (Média Servidor: {(avg_hs*100):.1f}%, Desvio: {(std_dev*100):.1f}%)"
                    
                    await send_discord_alert(s.player.fivem_id, s.player.nickname, rate_str, reason_str)

        await db.commit()

@celery_app.task(name="tasks.analyze_global_deviations")
def analyze_global_deviations():
    """Task Celery que dispara a auditoria global noturna."""
    asyncio.run(async_run_z_score())
