"""Listas de apoyo para la interfaz: categorías y técnicos disponibles."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.categoria import Categoria
from src.entities.usuario import Usuario
from src.utils import reglas


def listar_categorias(db: Session):
    return db.execute(select(Categoria).order_by(Categoria.tipo, Categoria.nombre)).scalars().all()


def listar_tecnicos(db: Session):
    return db.execute(
        select(Usuario)
        .where(Usuario.rol == reglas.ROL_TECNICO, Usuario.activo.is_(True))
        .order_by(Usuario.nombre)
    ).scalars().all()