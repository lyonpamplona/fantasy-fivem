"""Schemas Pydantic compartilhados pelas entradas de admin/webhook."""

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    """Contrato de payload esperado de webhooks externos de partida."""

    killer_id: str
    victim_id: str
    headshot: bool
    weapon: str
    distance_meters: float
    bone_hit_id: int
    ttk_ms: int
    timestamp: int
    nonce: str
