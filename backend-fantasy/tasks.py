"""Tasks Celery para processamento assincrono de eventos de partida."""

import json
import os

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from celery_app import celery_app
from models import Card, Player
from utils import alert_server_moderation

DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")
engine = create_engine(DATABASE_URL_SYNC)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_client = redis.from_url(os.getenv("REDIS_URL"))

@celery_app.task(name="process_match_event")
def process_match_event(payload: dict):
    """Processa um unico evento de partida e atualiza o estado de jogador/cards."""
    db = SessionLocal()
    try:
        killer_id = payload['killer_id']
        headshot = payload['headshot']
        distance = payload['distance_meters']
        bone = payload['bone_hit_id']
        ttk = payload['ttk_ms']

        killer = db.query(Player).filter(Player.fivem_id == killer_id).first()
        if not killer or killer.is_quarantined:
            return

        if headshot and distance > 150.0 and bone == 31086 and ttk < 200:
            if not killer.is_monitored:
                killer.is_monitored = True
                db.commit()
                alert_server_moderation(killer.fivem_id, killer.nickname, "Múltiplos gatilhos de DMA/Aimbot acionados (Distância Extrema + Head Bone Exato + TTK Anormal).")
                return
            else:
                killer.is_quarantined = True
                db.commit()
                alert_server_moderation(killer.fivem_id, killer.nickname, "Quarentena Definitiva. Anomalias continuaram após monitoramento inicial.")
                return

        cards = db.query(Card).filter(Card.owner_id == killer.id).all()
        multipliers = {'COMMON': 1.0, 'RARE': 1.2, 'EPIC': 1.5, 'LEGENDARY': 2.0}
        updated_cards = []

        for card in cards:
            base_points = 7 if headshot else 5
            multiplier = multipliers.get(card.rarity, 1.0)
            if killer.is_vip:
                multiplier += 0.15
                
            card.xp += int(base_points * multiplier)
            card.kills += 1
            if headshot:
                card.headshots += 1

            if card.xp >= (card.level * 1000):
                if card.rarity == 'RARE' and not killer.squad_id:
                    card.xp = card.level * 1000
                else:
                    card.level += 1
            
            updated_cards.append({"card_id": card.id, "xp": card.xp, "level": card.level, "kills": card.kills})

        db.commit()
        redis_client.publish("ws_card_updates", json.dumps(updated_cards))
    finally:
        db.close()
