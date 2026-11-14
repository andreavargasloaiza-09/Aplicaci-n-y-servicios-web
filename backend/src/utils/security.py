"""Contraseñas (bcrypt), tokens JWT y verificación de permisos por scopes (RF-10, RNF-06)."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from src.utils.config import settings
from src.database.connection import get_db
from src.entities.usuario import Usuario
from src.utils.reglas import DESCRIPCION_SCOPES, SCOPES_POR_ROL

# auto_error=False: el mensaje de "sin token" lo damos nosotros, en español.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", scopes=DESCRIPCION_SCOPES, auto_error=False
)


@dataclass
class Sesion:
    """Quién hace la solicitud y con qué permisos (los scopes salen del token)."""

    usuario: Usuario
    scopes: list


def _a_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:72]   # bcrypt solo usa los primeros 72 bytes


def hashear_password(password: str) -> str:
    return bcrypt.hashpw(_a_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(_a_bytes(password), password_hash.encode("utf-8"))
    except ValueError:
        return False


def crear_token(usuario: Usuario) -> str:
    """El token lleva el id del usuario, su rol y sus scopes (HU-01)."""
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(usuario.id),
        "rol": usuario.rol,
        "scopes": SCOPES_POR_ROL[usuario.rol],
        "exp": expira,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def obtener_sesion(
    security_scopes: SecurityScopes,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Sesion:
    """Dependencia de FastAPI: valida el token y exige los scopes pedidos por el endpoint."""
    no_autenticado = HTTPException(
        status_code=401,
        detail="Credenciales no válidas o sesión vencida",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise no_autenticado
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario_id = int(payload.get("sub"))
    except (jwt.PyJWTError, TypeError, ValueError):
        raise no_autenticado

    usuario = db.get(Usuario, usuario_id)
    if usuario is None or not usuario.activo:
        raise no_autenticado

    scopes_token = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in scopes_token:
            raise HTTPException(status_code=403, detail="No tiene permisos para esta operación")
    return Sesion(usuario=usuario, scopes=scopes_token)
