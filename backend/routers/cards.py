import random

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import verify_token
from database import get_db
from models import Card, Player

router = APIRouter()


@router.get("/user/me/profile")
async def get_my_profile(user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Player).where(Player.fivem_id == user_id)
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        return {"wallet_balance": 0}
    return {"wallet_balance": user.wallet_balance}


@router.get("/user/me")
async def get_my_cards(user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt_user = select(Player).where(Player.fivem_id == user_id)
    user = (await db.execute(stmt_user)).scalars().first()
    if not user:
        return []

    stmt_cards = select(Card).where(Card.owner_id == user.id)
    cards = (await db.execute(stmt_cards)).scalars().all()
    if not cards:
        return []

    nicknames = list(set([c.player_nickname for c in cards]))
    stmt_pros = select(Player.nickname, Player.is_monitored).where(Player.nickname.in_(nicknames))
    pros_result = await db.execute(stmt_pros)
    monitored_map = {row.nickname: row.is_monitored for row in pros_result.all()}

    result = []
    for c in cards:
        result.append(
            {
                "id": c.id,
                "rarity": c.rarity,
                "serial_number": c.serial_number,
                "level": c.level,
                "xp": c.xp,
                "kills": c.kills,
                "headshots": getattr(c, "headshots", 0),
                "float_value": getattr(c, "float_value", 0.5000),
                "player_nickname": c.player_nickname,
                "is_monitored": monitored_map.get(c.player_nickname, False),
            }
        )
    return result


@router.post("/burn")
async def burn_cards(card_ids: list[int] = Body(...), user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    if len(card_ids) != 10:
        raise HTTPException(status_code=400, detail="Voce deve fornecer exatamente 10 cartas.")
    if len(set(card_ids)) != 10:
        raise HTTPException(status_code=400, detail="IDs duplicados nao sao permitidos na forja.")

    stmt = select(Player).where(Player.fivem_id == user_id)
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Jogador nao encontrado")

    stmt_cards = select(Card).where(Card.id.in_(card_ids), Card.owner_id == user.id, Card.rarity == "COMMON")
    cards = (await db.execute(stmt_cards)).scalars().all()
    if len(cards) != 10:
        raise HTTPException(
            status_code=400,
            detail="Cartas invalidas. Certifique-se de que possui todas e sao COMMON.",
        )

    total_xp = sum(c.xp for c in cards)
    burned_names = [c.player_nickname for c in cards]

    exodia_roster = ["FalleN", "fer", "TACO", "coldzera", "fnx"]
    is_special_combo = all(player in burned_names for player in exodia_roster)

    if is_special_combo:
        new_rarity = "LEGENDARY"
        new_player = "LG Major Winner '16"
    else:
        roll = random.random()
        if roll < 0.02:
            new_rarity = "LEGENDARY"
        elif roll < 0.20:
            new_rarity = "EPIC"
        else:
            new_rarity = "RARE"

        pro_players = ["FalleN", "KSCERATO", "fer", "coldzera", "TACO", "fnx", "arT", "yuurih", "chelo", "VINI"]
        new_player = random.choice(pro_players)

    base_float = random.uniform(0.1000, 0.9999)
    xp_discount = (total_xp / 1000) * 0.015
    final_float = max(0.0001, base_float - xp_discount)

    for card in cards:
        await db.delete(card)

    new_card = Card(
        owner_id=user.id,
        player_nickname=new_player,
        rarity=new_rarity,
        serial_number=random.randint(10000, 99999),
        level=1,
        xp=0,
        kills=0,
        headshots=0,
        float_value=round(final_float, 4),
    )

    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)

    return {
        "id": new_card.id,
        "rarity": new_card.rarity,
        "serial_number": new_card.serial_number,
        "player_nickname": new_card.player_nickname,
        "float_value": new_card.float_value,
        "level": new_card.level,
        "xp": new_card.xp,
        "kills": new_card.kills,
        "headshots": new_card.headshots,
        "is_special": is_special_combo,
    }
