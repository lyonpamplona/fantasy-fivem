from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import List
from database import get_db
from models import Player, Card
from routers.auth import get_current_user
from routers.packs import COST_MAP
import random
import uuid

router = APIRouter()

class CardRole(BaseModel):
    card_id: int
    role: str

class SquadUpdate(BaseModel):
    squad: List[CardRole]

@router.get("/user/me")
async def get_my_cards(db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    cards = (await db.execute(select(Card).options(selectinload(Card.market_listing)).where(Card.owner_id == current_player.id))).scalars().all()
    return [{
        "id": c.id, "serial_number": c.serial_number, "player_nickname": c.player_nickname,
        "rarity": c.rarity, "level": c.level, "kills": c.kills, "headshots": c.headshots,
        "float_value": c.float_value, "squad_position": c.squad_position,
        "squad_role": getattr(c, 'squad_role', None),
        "deployment_cost": c.deployment_cost, "contract_points": c.contract_points,
        "is_listed": c.market_listing is not None,
        "listing_id": c.market_listing.id if c.market_listing else None
    } for c in cards]

@router.post("/user/me/squad")
async def update_squad(payload: SquadUpdate, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if len(payload.squad) > 5:
        raise HTTPException(status_code=400)
    
    card_ids = [item.card_id for item in payload.squad]
    
    selected_cards = (await db.execute(
        select(Card).options(selectinload(Card.market_listing)).where(Card.id.in_(card_ids), Card.owner_id == current_player.id)
    )).scalars().all()
    
    if len(selected_cards) != len(card_ids):
        raise HTTPException(status_code=400)
        
    for c in selected_cards:
        if c.market_listing is not None:
            raise HTTPException(status_code=400)
        if c.contract_points <= 0 and c.squad_position is None:
            raise HTTPException(status_code=400)
            
    total_cost = sum(c.deployment_cost for c in selected_cards)
    if total_cost > 100:
        raise HTTPException(status_code=400)
        
    current_squad = (await db.execute(
        select(Card).where(Card.owner_id == current_player.id, Card.squad_position != None)
    )).scalars().all()
    
    for c in current_squad:
        c.squad_position = None
        c.squad_role = None
        
    for i, item in enumerate(payload.squad):
        card = next(c for c in selected_cards if c.id == item.card_id)
        card.squad_position = i + 1
        card.squad_role = item.role
        if card.contract_points > 0:
            card.contract_points -= 1
        
    await db.commit()
    return {"status": "success", "total_cost": total_cost}

@router.post("/burn")
async def burn_cards(card_ids: List[int], db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if not (5 <= len(card_ids) <= 10):
        raise HTTPException(status_code=400)

    cards_to_burn = (await db.execute(
        select(Card).options(selectinload(Card.market_listing)).where(Card.id.in_(card_ids), Card.owner_id == current_player.id)
    )).scalars().all()

    if len(cards_to_burn) != len(card_ids):
        raise HTTPException(status_code=400)

    for c in cards_to_burn:
        if c.squad_position is not None or c.market_listing is not None:
            raise HTTPException(status_code=400)

    rarities = [c.rarity for c in cards_to_burn]
    dominant_rarity = max(set(rarities), key=rarities.count)
    upgrade_map = {"COMMON": "RARE", "RARE": "EPIC", "EPIC": "LEGENDARY", "LEGENDARY": "LEGENDARY"}
    new_rarity = upgrade_map.get(dominant_rarity, "RARE")

    for c in cards_to_burn:
        await db.delete(c)

    success_chance = {5: 20, 6: 36, 7: 52, 8: 68, 9: 84, 10: 100}.get(len(card_ids), 0)
    roll = random.randint(1, 100)

    if roll > success_chance:
        await db.commit()
        return {"status": "failed"}

    new_card = Card(
        owner_id=current_player.id,
        serial_number=str(uuid.uuid4()).split("-")[0].upper(),
        player_nickname=f"FORGED_{random.randint(100,999)}",
        rarity=new_rarity,
        level=1,
        kills=random.randint(30, 100),
        headshots=random.randint(10, 50),
        float_value=round(random.uniform(0.001, 0.050), 4),
        deployment_cost=COST_MAP.get(new_rarity, 10),
        contract_points=7
    )
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)

    return {
        "status": "success",
        "card": {
            "id": new_card.id, "serial_number": new_card.serial_number, "player_nickname": new_card.player_nickname,
            "rarity": new_card.rarity, "level": new_card.level, "kills": new_card.kills, "headshots": new_card.headshots,
            "float_value": new_card.float_value, "deployment_cost": new_card.deployment_cost, "contract_points": new_card.contract_points
        }
    }