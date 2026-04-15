import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Player
from auth import create_access_token

router = APIRouter()
ALLOWED_DEV_ENVS = {"development", "dev", "local", "test"}


def is_dev_login_enabled():
    app_env = os.getenv("APP_ENV", "development").lower()
    flag = os.getenv("ENABLE_DEV_LOGIN", "false").lower() in {"1", "true", "yes", "on"}
    return flag and app_env in ALLOWED_DEV_ENVS

@router.get("/dev-login/{steam_id}")
async def dev_login(steam_id: str, db: AsyncSession = Depends(get_db)):
    if not is_dev_login_enabled():
        raise HTTPException(status_code=404, detail="Rota nao disponivel neste ambiente")

    stmt = select(Player).where(Player.fivem_id == steam_id)
    result = await db.execute(stmt)
    player = result.scalars().first()
    if not player:
        player = Player(
            fivem_id=steam_id,
            nickname="Player_Teste",
            wallet_balance=100000.0,
            suspicion_score=0.0
        )
        db.add(player)
        await db.commit()
        await db.refresh(player)
    token = create_access_token({"sub": steam_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "player": player.nickname
    }
