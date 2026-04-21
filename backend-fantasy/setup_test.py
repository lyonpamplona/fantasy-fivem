"""Auxiliar de seed para testes manuais locais dos fluxos de auth/perfil."""

import asyncio
import os
from datetime import datetime, timedelta

import jwt
from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import Player

async def setup_test():
    """Garante que um jogador de teste exista e imprime um JWT valido."""
    async with AsyncSessionLocal() as db:
        # 1. Tenta achar o jogador 100
        stmt = select(Player).where(Player.fivem_id == "100")
        result = await db.execute(stmt)
        player = result.scalars().first()

        # 2. Se não existe, cria. Se existe, atualiza o saldo.
        if not player:
            player = Player(fivem_id="100", nickname="Tester Magnata", wallet_balance=5000.0)
            db.add(player)
        else:
            player.wallet_balance = 5000.0
            player.nickname = "Tester Magnata"
            
        await db.commit()
        
        # 3. Gera o Token JWT Criptografado
        secret = os.getenv("JWT_SECRET")
        expire = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode({"sub": "100", "exp": expire}, secret, algorithm="HS256")
        
        print("\n" + "="*50)
        print("✅ JOGADOR PRONTO E COM 5000 COINS!")
        print("🔑 COPIE SEU TOKEN ABAIXO:\n")
        print(token)
        print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(setup_test())
