import os
import jwt
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Player
from auth import create_access_token

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")
ALGORITHM = "HS256"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)):
    try:
        # Decodifica o crachá do jogador
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        steam_id: str = payload.get("sub")
        if steam_id is None:
            raise HTTPException(status_code=401, detail="Token corrompido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Busca o jogador no banco de dados
    result = await db.execute(select(Player).where(Player.fivem_id == steam_id))
    player = result.scalars().first()
    
    # 🚨 O SEGREDO (Auto-Heal / God Mode) 🚨
    # Se você limpou a DB, mas o navegador ainda tem o Token, recriamos o jogador na hora!
    if not player:
        player = Player(
            fivem_id=steam_id,
            nickname=f"Operador_{steam_id[-4:]}",
            wallet_balance=1000000.0,  # 1 Milhão garantido para testes
            is_vip=True
        )
        db.add(player)
        await db.commit()
        await db.refresh(player)
        
    return player

@router.get("/dev-login/{steam_id}")
async def dev_login(steam_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Player).where(Player.fivem_id == steam_id)
    result = await db.execute(stmt)
    player = result.scalars().first()
    
    if not player:
        player = Player(
            fivem_id=steam_id,
            nickname=f"User_{steam_id.split(':')[1] if ':' in steam_id else steam_id}",
            wallet_balance=1000000.0,
            suspicion_score=0.0
        )
        db.add(player)
        await db.commit()
        await db.refresh(player)

    token = create_access_token({"sub": steam_id})
    return {
        "message": "Auth_OK",
        "access_token": token,
        "token_type": "bearer",
        "player": player.nickname
    }