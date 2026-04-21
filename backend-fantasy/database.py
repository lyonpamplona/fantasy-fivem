"""Utilitarios de bootstrap do banco para o servico de gameplay fantasy."""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("ERRO CRÍTICO: DATABASE_URL não encontrada no arquivo .env")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    """Fornece uma sessao assincrona do SQLAlchemy por requisicao."""
    async with AsyncSessionLocal() as session:
        yield session
