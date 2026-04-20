import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET nao definida no .env")

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_in: timedelta | None = None):
    to_encode = data.copy()
    expire_at = datetime.now(timezone.utc) + (expires_in or timedelta(days=7))
    to_encode.update({"exp": expire_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_admin_token():
    return create_access_token(
        {"sub": "admin", "role": "admin"},
        expires_in=timedelta(hours=12),
    )


def _extract_token_from_request(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return token

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]

    return None


def _decode_or_unauthorized(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Token invalido") from exc


async def verify_token(request: Request):
    token = _extract_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    payload = _decode_or_unauthorized(token)
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Token sem identificador de usuario")

    return subject


async def verify_admin_token(request: Request):
    token = _extract_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    payload = _decode_or_unauthorized(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permissao insuficiente")

    return payload
