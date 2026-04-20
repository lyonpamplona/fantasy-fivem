from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from database import get_db
from models import Player, Card, MarketListing, PlayerPack
from routers.auth import get_current_user
import time
import math
from datetime import datetime, timedelta

router = APIRouter()

class SellRequest(BaseModel):
    price: int
    is_auction: bool = False

class BuyStoreRequest(BaseModel):
    expected_price: int

class BidRequest(BaseModel):
    bid_amount: int

BASE_PACK_PRICES = {
    "1": 1000,
    "3": 2800,
    "5": 4500,
    "7": 6000,
    "10": 8000
}

DARKWEB_PACK_PRICE = 50000

def calculate_dynamic_price(pack_type: str, base_price: int) -> dict:
    current_hour = int(time.time() / 3600)
    seed = current_hour + int(pack_type)
    fluctuation_multiplier = math.sin(seed) 
    fluctuation_percentage = round(fluctuation_multiplier * 15.0, 1) 
    current_price = int(base_price * (1 + (fluctuation_percentage / 100.0)))
    
    return {
        "pack_type": pack_type,
        "base_price": base_price,
        "current_price": current_price,
        "fluctuation": fluctuation_percentage
    }

def generate_mock_history(card_id: int, base_price: int) -> list:
    history = []
    current_day = int(time.time() / 86400)
    for i in range(7, -1, -1):
        day_seed = current_day - i + card_id
        variance = math.sin(day_seed) * 0.25 
        price = int(base_price * (1 + variance))
        date_str = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        history.append({"date": date_str, "price": max(100, price)})
    return history

@router.get("/store")
async def get_store_prices():
    packs = []
    for p_type, base_price in BASE_PACK_PRICES.items():
        packs.append(calculate_dynamic_price(p_type, base_price))
    return packs

@router.post("/buy/{pack_type}")
async def buy_store_pack(pack_type: str, payload: BuyStoreRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if pack_type not in BASE_PACK_PRICES:
        raise HTTPException(status_code=400, detail="Tipo de pacote inválido.")
        
    dynamic_data = calculate_dynamic_price(pack_type, BASE_PACK_PRICES[pack_type])
    actual_price = dynamic_data["current_price"]
    
    if payload.expected_price != actual_price:
        raise HTTPException(status_code=400, detail="A cotação do mercado foi alterada. Atualize a página.")

    if current_player.wallet_balance < actual_price:
        raise HTTPException(status_code=400, detail="Fundos insuficientes na carteira.")

    current_player.wallet_balance -= actual_price
    result = await db.execute(select(PlayerPack).where(PlayerPack.owner_id == current_player.id, PlayerPack.pack_type == pack_type))
    existing_pack = result.scalars().first()

    if existing_pack:
        existing_pack.amount += 1
    else:
        new_pack = PlayerPack(owner_id=current_player.id, pack_type=pack_type, amount=1)
        db.add(new_pack)

    await db.commit()
    return {"status": "success", "new_balance": current_player.wallet_balance}

@router.get("/p2p")
async def get_p2p_listings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MarketListing).options(selectinload(MarketListing.card)).where(MarketListing.is_active == True)
    )
    return result.scalars().all()

@router.get("/p2p/history/{card_id}")
async def get_card_market_history(card_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalars().first()
    if not card:
        raise HTTPException(status_code=404, detail="Ativo não encontrado.")
    base_valuation = card.deployment_cost * 1500
    history_data = generate_mock_history(card.id, base_valuation)
    return history_data

@router.post("/p2p/sell/{card_id}")
async def sell_card(card_id: int, payload: SellRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.id == card_id, Card.owner_id == current_player.id))
    card = result.scalars().first()

    if not card or card.squad_position is not None:
        raise HTTPException(status_code=400, detail="Carta em uso no esquadrão ou não encontrada.")

    listing_check = await db.execute(select(MarketListing).where(MarketListing.card_id == card.id, MarketListing.is_active == True))
    if listing_check.scalars().first():
        raise HTTPException(status_code=400, detail="Esta carta já está ativa no mercado.")

    new_listing = MarketListing(
        card_id=card.id, 
        seller_id=current_player.id, 
        price=payload.price, 
        is_active=True,
        is_auction=payload.is_auction
    )
    db.add(new_listing)
    await db.commit()
    return {"status": "success"}

@router.post("/p2p/buy/{listing_id}")
async def buy_p2p_card(listing_id: int, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(MarketListing).options(selectinload(MarketListing.card)).where(MarketListing.id == listing_id, MarketListing.is_active == True))
    listing = result.scalars().first()

    if not listing:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    if listing.is_auction:
        raise HTTPException(status_code=400, detail="Este ativo está em modo de Leilão. Utilize a licitação.")
    if listing.seller_id == current_player.id:
        raise HTTPException(status_code=400, detail="Ação bloqueada: Não pode adquirir o próprio ativo.")
    if current_player.wallet_balance < listing.price:
        raise HTTPException(status_code=400, detail="Capital insuficiente para executar a ordem.")

    seller_result = await db.execute(select(Player).where(Player.id == listing.seller_id))
    seller = seller_result.scalars().first()

    current_player.wallet_balance -= listing.price
    if seller:
        seller.wallet_balance += listing.price

    listing.card.owner_id = current_player.id
    listing.card.squad_position = None 
    listing.is_active = False

    await db.commit()
    return {"status": "success", "new_balance": current_player.wallet_balance}

@router.post("/p2p/bid/{listing_id}")
async def place_bid(listing_id: int, payload: BidRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(MarketListing).where(MarketListing.id == listing_id, MarketListing.is_active == True))
    listing = result.scalars().first()

    if not listing or not listing.is_auction:
        raise HTTPException(status_code=400, detail="Este ativo não está disponível para leilão.")
    if listing.seller_id == current_player.id:
        raise HTTPException(status_code=400, detail="Não pode licitar no próprio ativo.")

    min_required_bid = listing.current_bid if listing.current_bid else listing.price
    if payload.bid_amount <= min_required_bid:
        raise HTTPException(status_code=400, detail=f"A licitação deve ser superior a {min_required_bid} C$.")
    if current_player.wallet_balance < payload.bid_amount:
        raise HTTPException(status_code=400, detail="Capital insuficiente para cobrir o lance.")

    if listing.highest_bidder_id:
        previous_bidder_result = await db.execute(select(Player).where(Player.id == listing.highest_bidder_id))
        previous_bidder = previous_bidder_result.scalars().first()
        if previous_bidder:
            previous_bidder.wallet_balance += listing.current_bid

    current_player.wallet_balance -= payload.bid_amount
    listing.current_bid = payload.bid_amount
    listing.highest_bidder_id = current_player.id

    await db.commit()
    return {"status": "success", "new_balance": current_player.wallet_balance}

@router.delete("/p2p/cancel/{listing_id}")
async def cancel_listing(listing_id: int, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(MarketListing).where(MarketListing.id == listing_id, MarketListing.seller_id == current_player.id, MarketListing.is_active == True))
    listing = result.scalars().first()

    if not listing:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado ou não pertence ao utilizador.")
    if listing.is_auction and listing.highest_bidder_id:
        previous_bidder_result = await db.execute(select(Player).where(Player.id == listing.highest_bidder_id))
        previous_bidder = previous_bidder_result.scalars().first()
        if previous_bidder:
            previous_bidder.wallet_balance += listing.current_bid

    listing.is_active = False
    await db.commit()
    return {"status": "success"}

@router.get("/darkweb/status")
async def get_darkweb_status():
    current_hour = int(time.time() / 3600)
    is_active = (current_hour % 3) == 0 
    return {
        "is_active": is_active,
        "time_remaining_seconds": 3600 - (int(time.time()) % 3600) if is_active else 0,
        "pack_price": DARKWEB_PACK_PRICE
    }

@router.post("/darkweb/buy")
async def buy_darkweb_pack(db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    current_hour = int(time.time() / 3600)
    if (current_hour % 3) != 0:
        raise HTTPException(status_code=400, detail="O Node da Dark Web encontra-se inativo.")

    if current_player.wallet_balance < DARKWEB_PACK_PRICE:
        raise HTTPException(status_code=400, detail="Capital insuficiente. Fundos rejeitados.")

    current_player.wallet_balance -= DARKWEB_PACK_PRICE
    result = await db.execute(select(PlayerPack).where(PlayerPack.owner_id == current_player.id, PlayerPack.pack_type == "CLASSIFIED"))
    existing_pack = result.scalars().first()

    if existing_pack:
        existing_pack.amount += 1
    else:
        new_pack = PlayerPack(owner_id=current_player.id, pack_type="CLASSIFIED", amount=1)
        db.add(new_pack)

    await db.commit()
    return {"status": "success", "new_balance": current_player.wallet_balance}