"""Esquemas del historial de intervenciones."""
from typing import Optional

from pydantic import Field

from src.schemas.base import EntradaBase, FechaUTC, SalidaBase
from src.schemas.usuario import UsuarioSalida


class IntervencionCrear(EntradaBase):
    descripcion: str = Field(min_length=3, max_length=2000)


class IntervencionSalida(SalidaBase):
    id: int
    tipo: str
    descripcion: str
    estado_anterior: Optional[str] = None
    estado_nuevo: Optional[str] = None
    creado_en: FechaUTC
    autor: UsuarioSalida
