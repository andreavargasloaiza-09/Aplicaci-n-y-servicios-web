"""Esquemas de categoría."""
from src.schemas.base import SalidaBase


class CategoriaSalida(SalidaBase):
    id: int
    nombre: str
    tipo: str