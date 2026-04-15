import os
import random
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update
from dotenv import load_dotenv
from database import get_db
from models import Player, Card, AdminLog
from auth import create_admin_token, verify_admin_token

load_dotenv()

router = APIRouter()

@router.post("/login")
async def admin_login(password: str = Body(..., embed=True)):
    admin_secret = os.getenv("ADMIN_PASSWORD")
    if not admin_secret:
        raise HTTPException(status_code=500, detail="Configuração de segurança do servidor ausente.")
        
    if password != admin_secret:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return {"status": "success", "token": create_admin_token(), "token_type": "bearer"}

@router.get("/suspects")
async def get_suspects(
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Player).order_by(Player.suspicion_score.desc()).limit(50)
    players = (await db.execute(stmt)).scalars().all()
    
    result = []
    for p in players:
        stats_stmt = select(func.sum(Card.kills).label("total_kills"), func.sum(Card.headshots).label("total_hs")).where(Card.owner_id == p.id)
        stats = (await db.execute(stats_stmt)).first()
        total_kills = stats.total_kills or 0
        total_hs = stats.total_hs or 0
        hs_rate = (total_hs / total_kills * 100) if total_kills > 0 else 0
        
        result.append({
            "id": p.id,
            "fivem_id": p.fivem_id,
            "nickname": p.nickname,
            "kills": total_kills,
            "headshots": total_hs,
            "hs_rate": round(hs_rate, 1),
            "suspicion_score": round(p.suspicion_score, 1),
            "is_quarantined": p.is_quarantined,
            "is_monitored": p.is_monitored
        })
    return result

@router.post("/toggle_quarantine/{player_id}")
async def toggle_quarantine(
    player_id: int,
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Player).where(Player.id == player_id)
    player = (await db.execute(stmt)).scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player não encontrado")
    
    player.is_quarantined = not player.is_quarantined
    log = AdminLog(action="TOGGLE_QUARANTINE", target_player_id=player_id, details=f"Status alterado para: {player.is_quarantined}")
    db.add(log)
    await db.commit()
    return {"message": "Status de quarentena alterado", "is_quarantined": player.is_quarantined}

@router.get("/player/{player_id}/dossier")
async def get_player_dossier(
    player_id: int,
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Player).where(Player.id == player_id)
    player = (await db.execute(stmt)).scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player não encontrado")

    is_sus = player.suspicion_score > 60
    weapons = [{"name": "Heavy Sniper", "usage": 85}, {"name": "Special Carbine", "usage": 10}, {"name": "AP Pistol", "usage": 5}] if is_sus else [{"name": "Assault Rifle", "usage": 45}, {"name": "Combat PDW", "usage": 35}, {"name": "Pump Shotgun", "usage": 20}]
    avg_distance = random.randint(250, 450) if is_sus else random.randint(15, 60)
    reports = random.randint(12, 45) if is_sus else random.randint(0, 3)
    flags = ["Aimbot Lock Detectado (120ms)", "Wallhack: Tracing através de paredes", "Snap para cabeça anormal"] if is_sus else ["Nenhuma anomalia detectada"]

    return {
        "id": player.id,
        "nickname": player.nickname,
        "fivem_id": player.fivem_id,
        "suspicion_score": player.suspicion_score,
        "favorite_weapons": weapons,
        "avg_shot_distance": avg_distance,
        "reports": reports,
        "recent_flags": flags
    }

@router.post("/seed_mocks")
async def seed_mocks(
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    names = ["Klaus_Cheater", "AntiRecoil_User", "Legit_Player", "Pro_Sniper", "DMA_Ghost"]
    for name in names:
        is_sus = "Cheater" in name or "Recoil" in name or "Ghost" in name
        
        player = Player(
            fivem_id=f"steam:{random.randint(10000,99999)}",
            nickname=name,
            wallet_balance=10000,
            suspicion_score=random.randint(80, 100) if is_sus else random.randint(0, 15)
        )
        db.add(player)
        await db.flush()
        
        kills = random.randint(100, 500)
        hs = int(kills * (random.uniform(0.85, 0.98) if is_sus else random.uniform(0.2, 0.45)))
        float_val = round(random.uniform(0.0100, 0.5000) if is_sus else random.uniform(0.1500, 0.9999), 4)
        
        mock_card = Card(
            owner_id=player.id,
            player_nickname=name,
            rarity="LEGENDARY" if is_sus else "COMMON",
            serial_number=random.randint(1000, 9999),
            level=50,
            xp=50000,
            kills=kills,
            headshots=hs,
            float_value=float_val
        )
        db.add(mock_card)
        
    log = AdminLog(action="SEED_MOCKS", details="Emulação de dados executada")
    db.add(log)
    await db.commit()
    return {"message": "Cenários emulados!"}

@router.delete("/clear_mocks")
async def clear_mocks(
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    mock_names = ["Klaus_Cheater", "AntiRecoil_User", "Legit_Player", "Pro_Sniper", "DMA_Ghost"]
    stmt = select(Player).where(Player.nickname.in_(mock_names))
    players = (await db.execute(stmt)).scalars().all()
    
    for p in players:
        cards_stmt = select(Card).where(Card.owner_id == p.id)
        cards = (await db.execute(cards_stmt)).scalars().all()
        for c in cards:
            await db.delete(c)
        await db.delete(p)
        
    log = AdminLog(action="CLEAR_MOCKS", details="Dados emulados foram limpos")
    db.add(log)
    await db.commit()
    return {"message": "Logs de teste limpos!"}

@router.post("/inject_coins")
async def inject_coins(
    _admin_payload: dict = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(update(Player).values(wallet_balance=Player.wallet_balance + 500000))
    log = AdminLog(action="INJECT_COINS", details=f"Injeção global de 500k Coins para {result.rowcount} jogadores")
    db.add(log)
    await db.commit()
    return {"message": "Injeção concluída", "affected_players": result.rowcount}
