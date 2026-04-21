"""Modelos ORM compartilhados entre dominios Fantasy e Heuristica."""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ==========================================
# 1. CORE: JOGADORES (Partilhado por ambos)
# ==========================================
class Player(Base):
    """Conta principal do jogador com dados economicos e de risco."""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    fivem_id = Column(String, unique=True, index=True)
    nickname = Column(String)
    wallet_balance = Column(Integer, default=0)
    
    # Heurística
    suspicion_score = Column(Float, default=0.0)
    is_quarantined = Column(Boolean, default=False)
    is_vip = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relações Fantasy
    cards = relationship("Card", back_populates="owner", cascade="all, delete-orphan")
    packs = relationship("PlayerPack", back_populates="owner", cascade="all, delete-orphan")
    squads = relationship("Squad", back_populates="owner", cascade="all, delete-orphan")
    
    # Relações Heurística
    stats = relationship("PlayerStats", back_populates="player", uselist=False, cascade="all, delete-orphan")
    financial_logs = relationship("FinancialLog", back_populates="player", cascade="all, delete-orphan")


# ==========================================
# 2. ECOSSISTEMA FANTASY (Cartas, Mercado)
# ==========================================
class Card(Base):
    """Carta colecionavel/operador com progresso e estado de uso."""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    serial_number = Column(String, unique=True, index=True)
    
    player_nickname = Column(String)
    rarity = Column(String) # COMMON, RARE, EPIC, LEGENDARY, MYTHIC
    level = Column(Integer, default=1)
    
    # Atributos Visuais e Jogo
    kills = Column(Integer, default=0)
    headshots = Column(Integer, default=0)
    float_value = Column(Float, default=1.0)
    is_forged = Column(Boolean, default=False)
    
    # Contratos e Squad
    contract_points = Column(Integer, default=7)
    deployment_cost = Column(Integer, default=10)
    contract_end_date = Column(DateTime, nullable=True)
    squad_position = Column(Integer, nullable=True)

    owner = relationship("Player", back_populates="cards")
    market_listing = relationship("MarketListing", back_populates="card", uselist=False)

class PlayerPack(Base):
    """Inventario de packs nao abertos por jogador."""

    __tablename__ = "player_packs"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    pack_type = Column(String) # 1, 3, 5, 7, 10, CLASSIFIED
    amount = Column(Integer, default=1)

    owner = relationship("Player", back_populates="packs")

class MarketListing(Base):
    """Anuncio de mercado P2P para venda ou leilao de cartas."""

    __tablename__ = "market_listings"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    seller_id = Column(Integer, ForeignKey("players.id"))
    
    price = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Leilões
    is_auction = Column(Boolean, default=False)
    current_bid = Column(Integer, nullable=True)
    highest_bidder_id = Column(Integer, ForeignKey("players.id"), nullable=True)

    card = relationship("Card", back_populates="market_listing")


class Squad(Base):
    """Agrupamento tatico de jogador para composicao ativa."""

    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    name = Column(String, default="Alpha Squad")
    active = Column(Boolean, default=True)

    owner = relationship("Player", back_populates="squads")


# ==========================================
# 3. ECOSSISTEMA HEURÍSTICA (Anti-Cheat)
# ==========================================
class PlayerStats(Base):
    """Metrica consolidada de desempenho usada pela heuristica."""

    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    headshots = Column(Integer, default=0)
    torso = Column(Integer, default=0)
    arms = Column(Integer, default=0)
    legs = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    kd = Column(Float, default=1.0)
    
    # Gráfico de 7 Dias para a Dashboard
    kd_history = Column(JSON, default=list) 

    player = relationship("Player", back_populates="stats")

class FinancialLog(Base):
    """Log financeiro para trilha de auditoria anti-fraude."""

    __tablename__ = "financial_logs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    
    transaction_type = Column(String) # Ex: 'RMT_SUSPECT', 'MARKET_BUY', 'INJECT'
    target_id = Column(String)
    amount = Column(Integer, default=0)
    is_suspicious = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="financial_logs")
    
# ==========================================
# 4. SISTEMA DE AUDITORIA (Admin Logs)
# ==========================================
class AdminLog(Base):
    """Registro de acoes administrativas do painel."""

    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_username = Column(String, default="admin")
    action = Column(String)  # Ex: 'LOGIN', 'BAN', 'INJECT_COINS'
    target_id = Column(String, nullable=True) # ID do jogador afetado
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
