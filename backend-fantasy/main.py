import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, cards, packs, market, websocket, users, squad

app = FastAPI(title="Fantasy API - Game Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_GAME_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health/live")
async def health_check():
    return {"status": "alive", "service": "fantasy-game"}

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])
app.include_router(packs.router, prefix="/api/packs", tags=["Packs"])
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(users.router, prefix="/api/user", tags=["User"])
app.include_router(squad.router, prefix="/api/squad", tags=["squad"])
app.include_router(websocket.router, tags=["WS"])
