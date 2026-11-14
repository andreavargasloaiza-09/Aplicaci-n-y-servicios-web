"""Esquemas de usuario y de inicio de sesión."""
from pydantic import BaseModel

from src.schemas.base import SalidaBase


class UsuarioSalida(SalidaBase):
    id: int
    nombre: str
    correo: str
    rol: str


class TokenSalida(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioSalida
    scopes: list[str]