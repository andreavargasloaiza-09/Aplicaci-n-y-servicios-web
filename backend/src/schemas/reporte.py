"""Esquemas de los casos de soporte: lo que entra (validación en el servidor) y lo que sale."""
import re
from typing import Literal, Optional

from pydantic import Field, field_validator

from src.schemas.base import EntradaBase, FechaUTC, SalidaBase
from src.schemas.categoria import CategoriaSalida
from src.schemas.intervencion import IntervencionSalida
from src.schemas.usuario import UsuarioSalida


# ------------------------------------------------------------------ entrada
class ReporteCrear(EntradaBase):
    """RF-01 / RN-01 / RN-02: todos los campos son obligatorios."""

    descripcion: str = Field(min_length=5, max_length=2000, description="Descripción del fallo")
    placa: str = Field(min_length=1, max_length=50, description="Placa del equipo o recurso")
    telefono: str = Field(description="Teléfono de quien reporta")
    nombre_solicitante: str = Field(min_length=2, max_length=120)
    area: str = Field(min_length=2, max_length=100)
    categoria_id: int = Field(gt=0, description="Categoría del caso (ver GET /api/categorias)")

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor: str) -> str:
        limpio = re.sub(r"[\s\-]", "", valor)
        if not re.fullmatch(r"\+?\d{7,15}", limpio):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos (puede iniciar con +)")
        return limpio


class AsignarEntrada(EntradaBase):
    tecnico_id: int = Field(gt=0)


class TerminarEntrada(EntradaBase):
    respuesta: str = Field(min_length=5, max_length=2000, description="Respuesta final para el solicitante")


class CerrarEntrada(EntradaBase):
    motivo: Literal["resuelto", "error", "duplicado"]
    observacion: str = Field(min_length=3, max_length=1000)


class CalificarEntrada(EntradaBase):
    puntuacion: int = Field(ge=1, le=5)
    comentario: Optional[str] = Field(default=None, max_length=500)


# ------------------------------------------------------------------ salida
class ReporteResumen(SalidaBase):
    id: int
    estado: str
    categoria: CategoriaSalida
    placa: str
    nombre_solicitante: str
    area: str
    solicitante: UsuarioSalida
    tecnico: Optional[UsuarioSalida] = None
    creado_en: FechaUTC
    actualizado_en: FechaUTC
    cerrado_en: Optional[FechaUTC] = None


class ReporteDetalle(ReporteResumen):
    descripcion: str
    telefono: str
    respuesta_tecnica: Optional[str] = None
    motivo_cierre: Optional[str] = None
    observacion_cierre: Optional[str] = None
    calificacion: Optional[int] = None
    comentario_calificacion: Optional[str] = None
    intervenciones: list[IntervencionSalida] = []