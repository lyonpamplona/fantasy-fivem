from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    fivem_id = Column(String, unique=True, index=True)
    nickname = Column(String)
    is_vip = Column(Boolean, default=False)
    is_quarantined = Column(Boolean, default=False)
    is_monitored = Column(Boolean, default=False)
    suspicion_score = Column(Float, default=0.0)
    last_suspicion_update = Column(DateTime, default=func.now())
    wallet_balance = Column(Float, default=0.0)
    squad_id = Column(Integer, nullable=True)
    cards = relationship("Card", back_populates="owner")
    listings = relationship("MarketListing", back_populates="seller")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    player_nickname = Column(String)
    rarity = Column(String)
    serial_number = Column(Integer)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    headshots = Column(Integer, default=0)
    float_value = Column(Float, default=0.5)
    owner = relationship("Player", back_populates="cards")
    market_listing = relationship("MarketListing", back_populates="card", uselist=False)

class MarketListing(Base):
    __tablename__ = "market_listings"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), unique=True)
    seller_id = Column(Integer, ForeignKey("players.id"))
    price = Column(Float)
    created_at = Column(DateTime, default=func.now())
    card = relationship("Card", back_populates="market_listing")
    seller = relationship("Player", back_populates="listings")

class AdminLog(Base):
    __tablename__ = "admin_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    target_player_id = Column(Integer, nullable=True)
    details = Column(String)
    created_at = Column(DateTime, default=func.now())