from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Player
from auth import verify_token

router = APIRouter()

@router.get("/me/profile")
async def get_profile(user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(Player).where(Player.fivem_id == user_id))).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    return {
        "fivem_id": user.fivem_id,
        "nickname": user.nickname,
        "wallet_balance": user.wallet_balance
    }