from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import verify_token
from database import get_db
from models import Card, MarketListing, Player

router = APIRouter()


@router.get("/")
async def get_market_listings(db: AsyncSession = Depends(get_db)):
    stmt = select(MarketListing).join(Card)
    result = await db.execute(stmt)
    listings = result.scalars().all()
    return [
        {
            "id": listing.id,
            "price": listing.price,
            "card": {
                "id": listing.card.id,
                "player_nickname": listing.card.player_nickname,
                "rarity": listing.card.rarity,
                "float_value": listing.card.float_value,
            },
        }
        for listing in listings
    ]


@router.post("/sell")
async def list_card(
    card_id: int = Body(...),
    price: float = Body(...),
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    if price <= 0:
        raise HTTPException(status_code=400, detail="Preco invalido")

    stmt_user = select(Player).where(Player.fivem_id == user_id)
    user = (await db.execute(stmt_user)).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Jogador nao encontrado")

    stmt_card = select(Card).where(Card.id == card_id, Card.owner_id == user.id)
    card = (await db.execute(stmt_card)).scalars().first()
    if not card:
        raise HTTPException(status_code=404, detail="Carta nao encontrada")

    existing_listing = (await db.execute(select(MarketListing).where(MarketListing.card_id == card_id))).scalars().first()
    if existing_listing:
        raise HTTPException(status_code=409, detail="Carta ja listada no mercado")

    listing = MarketListing(card_id=card_id, seller_id=user.id, price=price)
    db.add(listing)
    await db.commit()
    return {"message": "Carta listada"}


@router.post("/buy/{listing_id}")
async def buy_card(listing_id: int, user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt_buyer = select(Player).where(Player.fivem_id == user_id)
    buyer = (await db.execute(stmt_buyer)).scalars().first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Jogador comprador nao encontrado")

    stmt_listing = select(MarketListing).where(MarketListing.id == listing_id)
    listing = (await db.execute(stmt_listing)).scalars().first()
    if not listing:
        raise HTTPException(status_code=404, detail="Item de mercado nao encontrado")

    if listing.seller_id == buyer.id:
        raise HTTPException(status_code=400, detail="Nao e permitido comprar sua propria carta")

    seller = (await db.execute(select(Player).where(Player.id == listing.seller_id))).scalars().first()
    if not seller:
        raise HTTPException(status_code=404, detail="Vendedor nao encontrado")

    card = (await db.execute(select(Card).where(Card.id == listing.card_id))).scalars().first()
    if not card:
        raise HTTPException(status_code=404, detail="Carta nao encontrada")
    if card.owner_id != seller.id:
        raise HTTPException(status_code=409, detail="Anuncio desatualizado, atualize o mercado")

    if buyer.wallet_balance < listing.price:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    buyer.wallet_balance -= listing.price
    seller.wallet_balance += listing.price
    card.owner_id = buyer.id
    await db.delete(listing)
    await db.commit()
    return {"message": "Compra realizada"}
