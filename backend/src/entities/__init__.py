"""Entidades (tablas). Se importan todas aquí para que SQLAlchemy conozca sus relaciones."""
from src.entities.usuario import Usuario
from src.entities.categoria import Categoria
from src.entities.reporte import Reporte
from src.entities.intervencion import Intervencion

__all__ = ["Usuario", "Categoria", "Reporte", "Intervencion"]
