"""Entidades (tablas). Se importan todas aquí para que SQLAlchemy conozca sus relaciones."""
from src.entities.usuario import Usuario
from src.entities.categoria import Categoria
from src.entities.reporte import Reporte
from src.entities.intervencion import Intervencion

_all_ = ["Usuario", "Categoria", "Reporte", "Intervencion"]