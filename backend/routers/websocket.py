import asyncio
import json
from contextlib import suppress

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from redis import asyncio as aioredis

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message):
        dead_connections = []
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection)


feed_manager = ConnectionManager()
cards_manager = ConnectionManager()

# Backwards compatibility for existing imports in packs.py.
manager = feed_manager

_redis_bridge_task: asyncio.Task | None = None


async def _redis_bridge_loop(redis_url: str):
    redis = aioredis.from_url(redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe("ws_card_updates")
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message.get("type") == "message":
                raw_data = message.get("data")
                if isinstance(raw_data, bytes):
                    raw_data = raw_data.decode("utf-8")

                try:
                    payload = json.loads(raw_data)
                except (TypeError, json.JSONDecodeError):
                    payload = {"type": "card_update", "data": raw_data}

                await cards_manager.broadcast(payload)

            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        raise
    finally:
        with suppress(Exception):
            await pubsub.unsubscribe("ws_card_updates")
        with suppress(Exception):
            await pubsub.close()
        with suppress(Exception):
            await redis.aclose()


async def start_redis_bridge(redis_url: str | None):
    global _redis_bridge_task
    if not redis_url:
        return
    if _redis_bridge_task and not _redis_bridge_task.done():
        return
    _redis_bridge_task = asyncio.create_task(_redis_bridge_loop(redis_url))


async def stop_redis_bridge():
    global _redis_bridge_task
    if not _redis_bridge_task:
        return

    _redis_bridge_task.cancel()
    with suppress(asyncio.CancelledError):
        await _redis_bridge_task
    _redis_bridge_task = None


@router.websocket("/ws/feed")
async def websocket_feed_endpoint(websocket: WebSocket):
    await feed_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        feed_manager.disconnect(websocket)


@router.websocket("/ws/cards")
async def websocket_cards_endpoint(websocket: WebSocket):
    await cards_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        cards_manager.disconnect(websocket)
