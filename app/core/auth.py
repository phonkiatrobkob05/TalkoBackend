from functools import lru_cache

import jwt
from fastapi import HTTPException, Request
from jwt import PyJWKClient

from app.core.config import settings


@lru_cache
def _jwks_client() -> PyJWKClient:
    return PyJWKClient(settings.supabase_jwks_url)


def _decode(token: str) -> dict:
    signing_key = _jwks_client().get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256", "RS256"],
        audience="authenticated",
        issuer=f"{settings.supabase_url}/auth/v1",
    )


def resolve_user_id(request: Request) -> str | None:
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        return None
    token = header[7:]
    try:
        claims = _decode(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return claims.get("sub")
