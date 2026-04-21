"""Worker de heuristica em tempo real para eventos de combate.

Aplica regras de suspeita, anti-boost e encaminha XP para o dominio Fantasy.
"""

import asyncio
import os
import time
from datetime import datetime

import aiohttp
from redis import asyncio as aioredis
from sqlalchemy.future import select

from celery_app import celery_app
from database import AsyncSessionLocal
from models import Player

async def send_discord_alert_live(player_id, nickname, score, reason):
    """Dispara alerta imediato de heuristica para o Discord."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return
    
    content = f"🚨 **ALERTA DE HEURÍSTICA** 🚨\n**Alvo:** `{nickname}` (ID: {player_id})\n**Score:** {score:.1f}/100\n**Gatilho:** {reason}\n**Ação:** Conta suspensa preventivamente e bloqueada no Fantasy."
    payload = {"content": content}
    
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)

async def async_process_event(data):
    """Processa evento de partida, calcula suspeita e aciona task de XP."""
    k_ip = data.get('killer_ip')
    v_ip = data.get('victim_ip')
    k_hwid = data.get('killer_hwid')
    v_hwid = data.get('victim_hwid')

    if (k_ip and v_ip and k_ip == v_ip) or (k_hwid and v_hwid and k_hwid == v_hwid):
        return

    async with AsyncSessionLocal() as db:
        stmt = select(Player).where(Player.fivem_id == data['killer_id'])
        result = await db.execute(stmt)
        killer = result.scalars().first()

        if not killer:
            return

        now = datetime.utcnow()
        if killer.last_suspicion_update:
            days_passed = (now - killer.last_suspicion_update).days
            if days_passed > 0:
                decay = days_passed * 5.0
                killer.suspicion_score = max(0.0, killer.suspicion_score - decay)
                if killer.suspicion_score < 85:
                    killer.is_monitored = False

        redis_client = aioredis.from_url(os.getenv("REDIS_URL"))
        
        current_window = int(time.time()) // 30
        window_key = f"window:{data['killer_id']}:{current_window}"
        kills_in_window = await redis_client.incr(window_key)
        
        if kills_in_window == 1:
            await redis_client.expire(window_key, 60)

        suspicion_bump = 0
        trigger_reason = "Múltiplas anomalias balísticas"

        if data.get('ttk_ms', 9999) < 150 and data.get('headshot'):
            suspicion_bump += 25
            trigger_reason = "Insta-Kill / Reação Desumana"
            
        if data.get('distance_meters', 0) > 100 and data.get('weapon') in ['WEAPON_PISTOL', 'WEAPON_SMG']:
            suspicion_bump += 20
            trigger_reason = "Distância impossível para a arma"
            
        if data.get('bone_hit_id') == 31086 and data.get('distance_meters', 0) > 50:
            suspicion_bump += 10

        if kills_in_window > 8:
            suspicion_bump += 50
            trigger_reason = "Hard Cap Biológico Excedido (>8 kills/30s)"

        was_monitored = killer.is_monitored

        if suspicion_bump > 0 or (killer.last_suspicion_update and (now - killer.last_suspicion_update).days > 0):
            killer.suspicion_score += suspicion_bump
            killer.last_suspicion_update = now
            if killer.suspicion_score >= 85:
                killer.is_monitored = True
                
            await db.commit()

        if killer.is_monitored and not was_monitored:
            await send_discord_alert_live(killer.fivem_id, killer.nickname, killer.suspicion_score, trigger_reason)

        if killer.is_monitored:
            await redis_client.aclose()
            return

        victim_id = data.get('victim_id')
        if victim_id:
            nemesis_key = f"nemesis:{data['killer_id']}:{victim_id}"
            kill_count = await redis_client.incr(nemesis_key)
            if kill_count == 1:
                await redis_client.expire(nemesis_key, 600)
            
            if kill_count > 3:
                await redis_client.aclose()
                return

        await redis_client.aclose()
        
    celery_app.send_task("fantasy.process_xp", args=[data])

@celery_app.task(name="process_match_event")
def process_match_event(data):
    """Task Celery de entrada para processamento heuristico realtime."""
    asyncio.run(async_process_event(data))
