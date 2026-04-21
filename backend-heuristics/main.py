"""Ponto de entrada principal do FastAPI para o servico de heuristica/admin."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import admin, webhook

app = FastAPI(title="Heuristics API - Admin Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        os.getenv("FRONTEND_ADMIN_URL", "http://localhost:5174")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health/live")
async def health_check():
    """Retorna status de vida para health checks de orquestracao."""
    return {"status": "alive", "service": "heuristics-admin"}

app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Webhook"])
