from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models import Player, Card
from routers.auth import get_current_user

router = APIRouter()

class DeployRequest(BaseModel):
    position: int
    role: str

@router.get("/")
async def get_squad(db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(
        select(Card)
        .where(Card.owner_id == current_player.id, Card.squad_position != None)
        .order_by(Card.squad_position)
    )
    return result.scalars().all()

@router.post("/deploy/{card_id}")
async def deploy_card(card_id: int, payload: DeployRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if payload.position < 1 or payload.position > 5:
        raise HTTPException(status_code=400, detail="Posição de esquadrão inválida.")
    
    valid_roles = ["Sniper", "Assault", "Support", "IGL", "Lurker"]
    if payload.role not in valid_roles:
        raise HTTPException(status_code=400, detail="Designação tática inválida.")

    result = await db.execute(select(Card).where(Card.id == card_id, Card.owner_id == current_player.id))
    card = result.scalars().first()

    if not card:
        raise HTTPException(status_code=404, detail="Ativo não encontrado no arsenal.")

    if getattr(card, 'contract_end_date', None) and card.contract_end_date > datetime.utcnow():
        raise HTTPException(status_code=400, detail="Operador encontra-se atualmente numa Operação Especial.")

    pos_check = await db.execute(
        select(Card).where(Card.owner_id == current_player.id, Card.squad_position == payload.position)
    )
    occupant = pos_check.scalars().first()
    if occupant:
        occupant.squad_position = None
        occupant.squad_role = None

    card.squad_position = payload.position
    card.squad_role = payload.role
    await db.commit()
    
    return {"status": "success"}

@router.post("/remove/{card_id}")
async def remove_card(card_id: int, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.id == card_id, Card.owner_id == current_player.id))
    card = result.scalars().first()
    
    if card:
        card.squad_position = None
        card.squad_role = None
        await db.commit()
        
    return {"status": "success"}