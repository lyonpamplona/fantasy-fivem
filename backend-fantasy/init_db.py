import asyncio
from database import engine, Base
from models import Player, Card, MarketListing, AdminLog

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_models())
