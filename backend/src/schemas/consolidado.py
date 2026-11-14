"""Esquema del consolidado de coordinación (CA-06)."""
from pydantic import BaseModel

from src.schemas.reporte import ReporteResumen


class ConsolidadoSalida(BaseModel):
    total: int
    abiertos: int
    cerrados: int
    por_estado: dict[str, int]
    casos_abiertos: list[ReporteResumen]
    casos_cerrados: list[ReporteResumen]
