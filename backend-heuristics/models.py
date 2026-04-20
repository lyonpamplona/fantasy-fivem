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
    listings = relationship("MarketListing", back_populates="seller", foreign_keys="MarketListing.seller_id")
    packs = relationship("PlayerPack", back_populates="owner")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    player_nickname = Column(String)
    rarity = Column(String)
    serial_number = Column(String)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    headshots = Column(Integer, default=0)
    float_value = Column(Float, default=0.5)
    
    squad_position = Column(Integer, nullable=True)
    squad_role = Column(String, nullable=True)
    deployment_cost = Column(Integer, default=10)
    contract_points = Column(Integer, default=7)

    owner = relationship("Player", back_populates="cards")
    market_listing = relationship("MarketListing", back_populates="card", uselist=False)

class MarketListing(Base):
    __tablename__ = "market_listings"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), unique=True)
    seller_id = Column(Integer, ForeignKey("players.id"))
    price = Column(Float)
    
    is_active = Column(Boolean, default=True)
    is_auction = Column(Boolean, default=False)
    current_bid = Column(Float, nullable=True)
    highest_bidder_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    card = relationship("Card", back_populates="market_listing")
    seller = relationship("Player", back_populates="listings", foreign_keys=[seller_id])
    highest_bidder = relationship("Player", foreign_keys=[highest_bidder_id])

class AdminLog(Base):
    __tablename__ = "admin_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    target_player_id = Column(Integer, nullable=True)
    details = Column(String)
    created_at = Column(DateTime, default=func.now())

class PlayerPack(Base):
    __tablename__ = "player_packs"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    pack_type = Column(String)
    amount = Column(Integer, default=0)
    owner = relationship("Player", back_populates="packs")

class MarketHistory(Base):
    __tablename__ = "market_history"
    id = Column(Integer, primary_key=True, index=True)
    rarity = Column(String)
    price = Column(Float)
    sold_at = Column(DateTime, default=func.now())

class BuyOrder(Base):
    __tablename__ = "buy_orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("players.id"))
    target_rarity = Column(String)
    max_price = Column(Float)
    created_at = Column(DateTime, default=func.now())