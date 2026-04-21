"""Gerenciador de conexoes WebSocket e endpoint de feed."""

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    """Registro em memoria de conexoes para broadcasts websocket."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Aceita e registra uma conexao websocket."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove o websocket do conjunto ativo quando desconectar."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Envia payload serializavel em JSON para todos os clientes ativos."""
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

@router.websocket("/ws/feed")
async def websocket_endpoint(websocket: WebSocket):
    """Mantem uma sessao websocket aberta para feeds em tempo real."""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def broadcast_drop(data: dict):
    """Publica um evento de drop para todos os clientes websocket conectados no momento."""
    await manager.broadcast(data)
