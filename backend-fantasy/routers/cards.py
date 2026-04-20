from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel
import random
import string
from datetime import datetime, timedelta

from database import get_db
from models import Player, Card
from routers.auth import get_current_user

router = APIRouter()

class ForgeRequest(BaseModel):
    card_ids: List[int]

class ContractRequest(BaseModel):
    duration_days: int

def generate_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.get("/user/me")
async def get_my_cards(db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.owner_id == current_player.id))
    return result.scalars().all()

@router.post("/forge")
async def forge_cards(payload: ForgeRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if len(payload.card_ids) != 5:
        raise HTTPException(status_code=400, detail="A Forja exige exatamente 5 operadores.")

    result = await db.execute(select(Card).where(Card.id.in_(payload.card_ids), Card.owner_id == current_player.id))
    cards_to_forge = result.scalars().all()

    if len(cards_to_forge) != 5:
        raise HTTPException(status_code=400, detail="Operadores inválidos ou não pertencem ao seu arsenal.")

    for card in cards_to_forge:
        if getattr(card, 'contract_end_date', None) and card.contract_end_date > datetime.utcnow():
            raise HTTPException(status_code=400, detail="Não pode forjar operadores em missão (Contrato).")
        if getattr(card, 'squad_position', None) is not None:
            raise HTTPException(status_code=400, detail="Remova os operadores do Esquadrão antes da Forja.")

    # Calcula o "Peso" do sacrifício para melhorar levemente as chances (FOMO)
    weight_map = {"COMMON": 1, "RARE": 3, "EPIC": 10, "LEGENDARY": 30, "MYTHIC": 100}
    total_weight = sum(weight_map.get(c.rarity, 1) for c in cards_to_forge)

    base_forge_cost = 1000
    if current_player.wallet_balance < base_forge_cost:
        raise HTTPException(status_code=400, detail=f"A Forja requer {base_forge_cost} C$.")
    current_player.wallet_balance -= base_forge_cost

    # Lógica RNG - Drop Aleatório com peso dinâmico
    chance_mythic = min(0.05, 0.005 + (total_weight * 0.0001))
    chance_legendary = min(0.15, 0.02 + (total_weight * 0.0005))
    chance_epic = min(0.30, 0.10 + (total_weight * 0.001))
    chance_rare = 0.35
    
    roll = random.random()
    if roll < chance_mythic:
        new_rarity = "MYTHIC"
    elif roll < chance_mythic + chance_legendary:
        new_rarity = "LEGENDARY"
    elif roll < chance_mythic + chance_legendary + chance_epic:
        new_rarity = "EPIC"
    elif roll < chance_mythic + chance_legendary + chance_epic + chance_rare:
        new_rarity = "RARE"
    else:
        new_rarity = "COMMON"

    # Apaga as cartas antigas
    for card in cards_to_forge:
        await db.delete(card)

    # Cria a nova carta
    new_card = Card(
        owner_id=current_player.id,
        player_nickname=cards_to_forge[0].player_nickname,
        rarity=new_rarity,
        serial_number=f"FRG-{generate_serial()}",
        is_forged=True,
        float_value=round(random.uniform(0.001, 0.999), 4),
        kills=random.randint(0, 50),
        headshots=random.randint(0, 20)
    )
    
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    
    return {"status": "success", "new_card": new_card, "new_balance": current_player.wallet_balance}

@router.post("/{card_id}/contract")
async def sign_contract(card_id: int, payload: ContractRequest, db: AsyncSession = Depends(get_db), current_player: Player = Depends(get_current_user)):
    if payload.duration_days not in [3, 7, 14]:
        raise HTTPException(status_code=400, detail="Duração de contrato inválida.")

    result = await db.execute(select(Card).where(Card.id == card_id, Card.owner_id == current_player.id))
    card = result.scalars().first()

    if not card:
        raise HTTPException(status_code=404, detail="Ativo não encontrado.")

    if getattr(card, 'contract_end_date', None) and card.contract_end_date > datetime.utcnow():
        raise HTTPException(status_code=400, detail="Ativo já se encontra em operação.")

    if card.squad_position is not None:
        raise HTTPException(status_code=400, detail="Retire o ativo do Esquadrão Tático antes de assinar contrato.")

    yield_multiplier = {"COMMON": 1.0, "RARE": 2.5, "EPIC": 5.0, "LEGENDARY": 12.0, "MYTHIC": 25.0}.get(card.rarity, 1.0)
    total_yield = (payload.duration_days * 150) * yield_multiplier

    card.contract_end_date = datetime.utcnow() + timedelta(days=payload.duration_days)
    card.contract_yield = total_yield

    await db.commit()
    return {"status": "success", "yield_expected": total_yield, "end_date": card.contract_end_date}