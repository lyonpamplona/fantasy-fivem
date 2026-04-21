import asyncio
from database import engine

async def init_models():
    async with engine.begin() as conn:
        pass

if __name__ == "__main__":
    asyncio.run(init_models())