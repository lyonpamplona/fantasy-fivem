import os
import random
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update
from dotenv import load_dotenv
from database import get_db
from models import Player, Card, AdminLog

load_dotenv()
router = APIRouter()

@router.post("/login")
async def admin_login(password: str = Body(..., embed=True)):
    admin_secret = os.getenv("ADMIN_PASSWORD")
    if not admin_secret or password != admin_secret:
        raise HTTPException(status_code=401, detail="Credencial invalida")
    return {"status": "success", "token": "access_granted_admin"}

@router.get("/suspects")
async def get_suspects(db: AsyncSession = Depends(get_db)):
    stmt = select(
        Player,
        func.coalesce(func.sum(Card.kills), 0).label('total_kills'),
        func.coalesce(func.sum(Card.headshots), 0).label('total_hs')
    ).outerjoin(Card, Player.id == Card.owner_id).group_by(Player.id).order_by(Player.suspicion_score.desc()).limit(50)
    
    records = (await db.execute(stmt)).all()
    result = []
    
    for player, tk, ths in records:
        hs_rate = (ths / tk * 100) if tk > 0 else 0
        result.append({
            "id": player.id, "fivem_id": player.fivem_id, "nickname": player.nickname,
            "kills": tk, "headshots": ths, "hs_rate": round(hs_rate, 1),
            "suspicion_score": round(player.suspicion_score, 1), "is_quarantined": player.is_quarantined
        })
    return result

@router.post("/toggle_quarantine/{player_id}")
async def toggle_quarantine(player_id: int, db: AsyncSession = Depends(get_db)):
    try:
        player = (await db.execute(select(Player).where(Player.id == player_id))).scalars().first()
        if not player:
            raise HTTPException(status_code=404)
        player.is_quarantined = not player.is_quarantined
        db.add(AdminLog(action="TOGGLE_QUARANTINE", target_player_id=player_id, details=str(player.is_quarantined)))
        await db.commit()
        return {"is_quarantined": player.is_quarantined}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{player_id}/dossier")
async def get_player_dossier(player_id: int, db: AsyncSession = Depends(get_db)):
    player = (await db.execute(select(Player).where(Player.id == player_id))).scalars().first()
    if not player:
        raise HTTPException(status_code=404)
    
    is_sus = player.suspicion_score > 60
    weapons = [{"name": "Heavy Sniper", "usage": 85}, {"name": "Special Carbine", "usage": 10}] if is_sus else [{"name": "Assault Rifle", "usage": 45}, {"name": "Pump Shotgun", "usage": 20}]
    
    hit_zones = {
        "head": random.randint(80, 98) if is_sus else random.randint(15, 30),
        "chest": random.randint(2, 15) if is_sus else random.randint(40, 65),
        "arms": random.randint(0, 3) if is_sus else random.randint(10, 20),
        "legs": random.randint(0, 2) if is_sus else random.randint(5, 15)
    }
    
    return {
        "id": player.id, "nickname": player.nickname, "fivem_id": player.fivem_id,
        "suspicion_score": player.suspicion_score, "favorite_weapons": weapons,
        "hit_zones": hit_zones,
        "avg_shot_distance": random.randint(250, 450) if is_sus else random.randint(15, 60),
        "reports": random.randint(12, 45) if is_sus else random.randint(0, 3),
        "recent_flags": ["Wallhack Detectado", "Aimbot Snap (Bone Lock)"] if is_sus else ["Sem anomalias detectadas"]
    }

@router.post("/seed_mocks")
async def seed_mocks(db: AsyncSession = Depends(get_db)):
    try:
        names = ["Klaus_Cheater", "Legit_Player", "DMA_Ghost", "Pro_Sniper"]
        for name in names:
            is_sus = "Cheater" in name or "Ghost" in name
            player = Player(fivem_id=f"steam:{random.randint(1000,9999)}", nickname=name, wallet_balance=10000, suspicion_score=90 if is_sus else 10)
            db.add(player)
            await db.flush()
            kills = random.randint(100, 500)
            hs = int(kills * (random.uniform(0.85, 0.98) if is_sus else random.uniform(0.2, 0.45)))
            mock_card = Card(owner_id=player.id, player_nickname=name, rarity="LEGENDARY" if is_sus else "COMMON", serial_number=str(random.randint(1000, 9999)), float_value=0.1, kills=kills, headshots=hs)
            db.add(mock_card)
        db.add(AdminLog(action="SEED_MOCKS", details="Mocks gerados"))
        await db.commit()
        return {"message": "Cenários emulados!"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear_mocks")
async def clear_mocks(db: AsyncSession = Depends(get_db)):
    try:
        players = (await db.execute(select(Player).where(Player.nickname.in_(["Klaus_Cheater", "Legit_Player", "DMA_Ghost", "Pro_Sniper"])))).scalars().all()
        for p in players:
            cards = (await db.execute(select(Card).where(Card.owner_id == p.id))).scalars().all()
            for c in cards:
                await db.delete(c)
            await db.delete(p)
        db.add(AdminLog(action="CLEAR_MOCKS", details="Mocks limpos"))
        await db.commit()
        return {"message": "Logs limpos!"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inject_coins")
async def inject_coins(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(update(Player).values(wallet_balance=Player.wallet_balance + 500000))
        db.add(AdminLog(action="INJECT_COINS", details=f"500k injetado em {result.rowcount} contas"))
        await db.commit()
        return {"affected_players": result.rowcount}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))