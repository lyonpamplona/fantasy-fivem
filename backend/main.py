import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from database import engine, Base
from routers import auth, admin, cards, packs, market, websocket, webhook


def _get_allowed_origins():
    configured_origins = os.getenv("CORS_ORIGINS", "")
    if configured_origins.strip():
        return [origin.strip().rstrip("/") for origin in configured_origins.split(",") if origin.strip()]

    app_env = os.getenv("APP_ENV", "development").lower()
    if app_env in {"development", "dev", "local", "test"}:
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ]

    return []


ALLOWED_ORIGINS = _get_allowed_origins()

app = FastAPI(title="Fantasy API")
app.state.limiter = packs.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=bool(ALLOWED_ORIGINS),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await websocket.start_redis_bridge(os.getenv("REDIS_URL"))


@app.on_event("shutdown")
async def shutdown():
    await websocket.stop_redis_bridge()

@app.get("/health/live")
async def health_check():
    return {"status": "alive"}

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])
app.include_router(packs.router, prefix="/api/packs", tags=["Packs"])
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(websocket.router, tags=["WS"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Webhook"])
