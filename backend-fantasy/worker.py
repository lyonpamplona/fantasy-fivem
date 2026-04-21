"""Implementacao alternativa de worker Celery para tratar eventos de partida."""

import asyncio
import json
import os
from datetime import datetime

from celery import Celery
from dotenv import load_dotenv
from redis import asyncio as aioredis
from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import Card, Player

load_dotenv()

celery_app = Celery(__name__, broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))

async def async_process_event(data):
    """Processa evento de partida de forma assincrona e publica atualizacoes de cards no Redis."""
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

        suspicion_bump = 0
        
        if data.get('ttk_ms', 9999) < 150 and data.get('headshot'):
            suspicion_bump += 25
            
        if data.get('distance_meters', 0) > 100 and data.get('weapon') in ['WEAPON_PISTOL', 'WEAPON_SMG']:
            suspicion_bump += 20
            
        if data.get('bone_hit_id') == 31086 and data.get('distance_meters', 0) > 50:
            suspicion_bump += 10

        if suspicion_bump > 0 or (killer.last_suspicion_update and (now - killer.last_suspicion_update).days > 0):
            killer.suspicion_score += suspicion_bump
            killer.last_suspicion_update = now
            if killer.suspicion_score >= 85:
                killer.is_monitored = True
                
            await db.commit()

        if killer.is_monitored:
            return

        stmt_cards = select(Card).where(Card.owner_id == killer.id)
        cards = (await db.execute(stmt_cards)).scalars().all()
        
        for card in cards:
            card.kills += 1
            if data.get('headshot'):
                card.headshots += 1
            
            card.xp += 10
            if data.get('headshot'):
                card.xp += 5
                
            if card.xp >= card.level * 1000:
                card.level += 1
                card.xp = 0

        await db.commit()

        redis_client = aioredis.from_url(os.getenv("REDIS_URL"))
        updates = []
        for card in cards:
            updates.append({
                "card_id": card.id,
                "xp": card.xp,
                "level": card.level,
                "kills": card.kills
            })
        if updates:
            await redis_client.publish("ws_card_updates", json.dumps(updates))
        await redis_client.aclose()

@celery_app.task(name="process_match_event")
def process_match_event(data):
    """Wrapper de task Celery para o processamento assincrono de eventos de partida."""
    asyncio.run(async_process_event(data))
