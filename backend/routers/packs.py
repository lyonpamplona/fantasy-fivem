import random
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from database import get_db
from models import Player, Card
from auth import verify_token
from routers.websocket import manager

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

PACK_COST = 2500
PRO_PLAYERS = ["FalleN", "KSCERATO", "fer", "coldzera", "TACO", "fnx", "arT", "yuurih", "chelo", "VINI", "HEN1", "boltz", "LUCAS1"]

@router.post("/open/STANDARD")
@limiter.limit("2/second")
async def open_standard_pack(
    request: Request,
    amount: int = Query(1), 
    user_id: str = Depends(verify_token), 
    db: AsyncSession = Depends(get_db)
):
    if amount not in [1, 3, 5, 7, 10]:
        raise HTTPException(status_code=400)

    stmt = select(Player).where(Player.fivem_id == user_id)
    player = (await db.execute(stmt)).scalars().first()
    
    if not player:
        player = Player(fivem_id=user_id, nickname="Player_Web", wallet_balance=500000, suspicion_score=0)
        db.add(player)
        await db.commit()
        await db.refresh(player)

    total_cost = PACK_COST * amount
    if player.wallet_balance < total_cost:
        raise HTTPException(status_code=400)

    player.wallet_balance -= total_cost
    new_cards = []
    
    for _ in range(amount):
        roll = random.random()
        if roll < 0.01: rarity = "LEGENDARY"
        elif roll < 0.05: rarity = "EPIC"
        elif roll < 0.20: rarity = "RARE"
        else: rarity = "COMMON"

        new_cards.append(Card(
            owner_id=player.id,
            player_nickname=random.choice(PRO_PLAYERS),
            rarity=rarity,
            serial_number=random.randint(10000, 99999),
            level=1,
            xp=0,
            kills=0,
            headshots=0,
            float_value=round(random.uniform(0.1500, 0.9999), 4) 
        ))

    db.add_all(new_cards)
    await db.commit()
    
    for c in new_cards:
        await db.refresh(c)
        if c.rarity in ["LEGENDARY", "EPIC"]:
            await manager.broadcast({
                "type": "drop",
                "player": player.nickname,
                "rarity": c.rarity,
                "card_player": c.player_nickname
            })

    return [
        {
            "id": c.id, "rarity": c.rarity, "serial_number": c.serial_number, 
            "player_nickname": c.player_nickname, "float_value": c.float_value, 
            "kills": c.kills, "headshots": c.headshots
        } for c in new_cards
    ]
