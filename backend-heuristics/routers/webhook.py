"""Endpoints de ingestao de webhook para telemetria de partida."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import Player

router = APIRouter()

@router.post("/match_event")
async def process_event(request: Request, db: AsyncSession = Depends(get_db)):
    """Processa um evento bruto de partida e incrementa as heuristicas de suspeita."""
    try:
        payload = await request.json()
        shooter_id = payload.get("shooter_id")
        headshot = payload.get("headshot", False)
        
        if not shooter_id:
            return {"status": "ignored", "reason": "No shooter_id"}
            
        player = (await db.execute(select(Player).where(Player.fivem_id == shooter_id))).scalars().first()
        
        if player:
            # Lógica Básica de Heurística MVP: Incrementa suspeita a cada Headshot
            if headshot:
                player.suspicion_score += 0.5
                if player.suspicion_score > 100:
                    player.suspicion_score = 100.0
            
            await db.commit()
            
        return {"status": "processed", "shooter": shooter_id}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
