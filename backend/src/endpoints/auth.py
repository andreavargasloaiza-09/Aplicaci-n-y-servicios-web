"""Autenticación: inicio de sesión y token JWT (HU-01, RF-10)."""
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.entities.usuario import Usuario
from src.utils.reglas import SCOPES_POR_ROL
from src.schemas.usuario import TokenSalida, UsuarioSalida
from src.utils.security import Sesion, crear_token, obtener_sesion, verificar_password

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenSalida, summary="Iniciar sesión")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """username es el correo del usuario."""
    correo = form.username.strip().lower()
    usuario = db.execute(select(Usuario).where(Usuario.correo == correo)).scalar_one_or_none()
    if usuario is None or not usuario.activo or not verificar_password(form.password, usuario.password_hash):
        # Mismo mensaje para correo inexistente y clave incorrecta (no revela cuál falló)
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSalida(
        access_token=crear_token(usuario),
        usuario=UsuarioSalida.model_validate(usuario),
        scopes=SCOPES_POR_ROL[usuario.rol],
    )


@router.get("/me", response_model=UsuarioSalida, summary="Usuario de la sesión actual")
def me(sesion: Sesion = Security(obtener_sesion)):
    return sesion.usuario