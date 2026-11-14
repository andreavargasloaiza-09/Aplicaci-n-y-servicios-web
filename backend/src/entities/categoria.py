"""Entidad Categoria: clasifica el caso y distingue incidente de solicitud."""
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base
from src.utils.reglas import TIPOS_CATEGORIA
from src.utils.sql import lista_sql


class Categoria(Base):
    __tablename__ = "categorias"
    __table_args__ = (
        CheckConstraint(f"tipo IN ({lista_sql(TIPOS_CATEGORIA)})", name="ck_categorias_tipo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    tipo: Mapped[str] = mapped_column(String(12))   # incidente | solicitud
