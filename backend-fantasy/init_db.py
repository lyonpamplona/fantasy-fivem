"""Script utilitario para inicializar tabelas do banco a partir dos metadados ORM."""

import asyncio

from database import Base, engine
from models import AdminLog, Card, MarketListing, Player

async def init_models():
    """Cria todas as tabelas mapeadas no banco configurado."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_models())
