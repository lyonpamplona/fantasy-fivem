from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Player, PlayerPack, Card
from routers.auth import get_current_user
import random  # <-- AQUI ESTÁ A FERRAMENTA DE SORTEIO
import uuid    # <-- AQUI ESTÁ O GERADOR DE IDs ÚNICOS

router = APIRouter()

PACK_CONFIG = {
    "1": {"amount": 1},
    "3": {"amount": 3},
    "5": {"amount": 5},
    "7": {"amount": 7},
    "10": {"amount": 10}
}

RARITY_WEIGHTS = {"COMMON": 60, "RARE": 25, "EPIC": 10, "LEGENDARY": 5}
COST_MAP = {"COMMON": 5, "RARE": 10, "EPIC": 15, "LEGENDARY": 30}

@router.get("/user/me")
async def get_my_packs(db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    packs = (await db.execute(select(PlayerPack).where(PlayerPack.owner_id == current_player.id))).scalars().all()
    return [{"id": p.id, "pack_type": p.pack_type, "amount": p.amount} for p in packs]

@router.post("/open/{pack_type}")
async def open_pack(pack_type: str, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if pack_type not in PACK_CONFIG:
        raise HTTPException(status_code=400)

    pack_record = (await db.execute(
        select(PlayerPack).where(PlayerPack.owner_id == current_player.id, PlayerPack.pack_type == pack_type)
    )).scalars().first()

    if not pack_record or pack_record.amount < 1:
        raise HTTPException(status_code=400)

    # Deduz o pacote do inventário
    pack_record.amount -= 1
    if pack_record.amount == 0:
        await db.delete(pack_record)

    generated_cards = []
    amount = PACK_CONFIG[pack_type]["amount"]

    # Gera as cartas aleatórias
    for _ in range(amount):
        chosen_rarity = random.choices(list(RARITY_WEIGHTS.keys()), weights=list(RARITY_WEIGHTS.values()))[0]
        float_val = round(random.uniform(0.001, 1.000), 4)
        
        new_card = Card(
            owner_id=current_player.id,
            serial_number=str(uuid.uuid4()).split("-")[0].upper(),
            player_nickname=f"TARGET_{random.randint(100, 999)}",
            rarity=chosen_rarity,
            level=1,
            kills=random.randint(0, 50),
            headshots=random.randint(0, 20),
            float_value=float_val,
            deployment_cost=COST_MAP.get(chosen_rarity, 5),
            contract_points=7
        )
        db.add(new_card)
        generated_cards.append(new_card)

    await db.commit()
    
    return {
        "status": "success",
        "cards": [{
            "id": c.id, "serial_number": c.serial_number, "player_nickname": c.player_nickname,
            "rarity": c.rarity, "level": c.level, "kills": c.kills, "headshots": c.headshots,
            "float_value": c.float_value, "deployment_cost": c.deployment_cost, "contract_points": c.contract_points
        } for c in generated_cards]
    }