"""Piezas comunes de los esquemas Pydantic."""
from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, PlainSerializer


def _a_iso_utc(valor: datetime) -> str:
    # SQLite devuelve fechas sin zona horaria; se marcan como UTC para que el navegador las convierta bien.
    if valor.tzinfo is None:
        valor = valor.replace(tzinfo=timezone.utc)
    return valor.astimezone(timezone.utc).isoformat()


FechaUTC = Annotated[datetime, PlainSerializer(_a_iso_utc, return_type=str, when_used="json")]

# Deben coincidir con utils/reglas.ESTADOS (se escriben aquí para que /docs muestre la lista desplegable)
EstadoCaso = Literal["reportado", "asignado", "en_reparacion", "terminado", "cerrado"]
GrupoCasos = Literal["abiertos", "cerrados"]


class EntradaBase(BaseModel):
    """Base de los datos que envía el cliente: recorta espacios al inicio y al final."""
    model_config = ConfigDict(str_strip_whitespace=True)


class SalidaBase(BaseModel):
    """Base de las respuestas: permite construirlas desde objetos de la base de datos."""
    model_config = ConfigDict(from_attributes=True)
