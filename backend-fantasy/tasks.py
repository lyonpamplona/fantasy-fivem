"""Tasks Celery de progressao de XP e atualizacao em tempo real.

Este modulo consome eventos processados pelo dominio de heuristica
e aplica evolucao de cards no dominio Fantasy.
"""

import json
import os

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from celery_app import celery_app
from models import Card, Player

DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")
engine = create_engine(DATABASE_URL_SYNC)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_client = redis.from_url(os.getenv("REDIS_URL"))

@celery_app.task(name="fantasy.process_xp")
def process_xp(payload: dict):
    """Processa XP/kills/headshots das cartas com base no evento da partida."""
    db = SessionLocal()
    try:
        killer_id = payload.get('killer_id')
        headshot = payload.get('headshot', False)

        killer = db.query(Player).filter(Player.fivem_id == killer_id).first()
        if not killer or killer.is_quarantined:
            return

        cards = db.query(Card).filter(Card.owner_id == killer.id).all()
        multipliers = {'COMMON': 1.0, 'RARE': 1.2, 'EPIC': 1.5, 'LEGENDARY': 2.0, 'MYTHIC': 3.0}
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
                    card.xp = 0
            
            updated_cards.append({
                "card_id": card.id,
                "xp": card.xp,
                "level": card.level,
                "kills": card.kills
            })

        db.commit()

        if updated_cards:
            redis_client.publish("ws_card_updates", json.dumps(updated_cards))

    finally:
        db.close()
