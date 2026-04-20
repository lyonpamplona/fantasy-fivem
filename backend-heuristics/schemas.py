from pydantic import BaseModel

class WebhookPayload(BaseModel):
    killer_id: str
    victim_id: str
    headshot: bool
    weapon: str
    distance_meters: float
    bone_hit_id: int
    ttk_ms: int
    timestamp: int
    nonce: str