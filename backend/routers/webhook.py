import os
import hmac
import hashlib
import time
from fastapi import APIRouter, HTTPException, Request
from schemas import WebhookPayload
from tasks import process_match_event

router = APIRouter()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_SECRET_BYTES = WEBHOOK_SECRET.encode() if WEBHOOK_SECRET else None

@router.post("/fivem")
async def process_webhook(payload: WebhookPayload, request: Request):
    if not WEBHOOK_SECRET_BYTES:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    current_time = int(time.time() * 1000)
    if abs(current_time - payload.timestamp) > 5000:
        raise HTTPException(status_code=403)

    signature = request.headers.get("X-Signature")
    if not signature:
        raise HTTPException(status_code=403)

    msg = f"{payload.killer_id}:{payload.victim_id}:{payload.timestamp}:{payload.nonce}".encode()
    expected_signature = hmac.new(WEBHOOK_SECRET_BYTES, msg, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403)

    if payload.killer_id == payload.victim_id:
        return {"status": "ignored"}

    process_match_event.delay(payload.model_dump())
    return {"status": "queued"}
