"""Entidad Usuario: solicitantes, técnicos y coordinadores."""
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base
from src.utils.fechas import ahora
from src.utils.reglas import ROLES
from src.utils.sql import lista_sql


class Usuario(Base):
    _tablename_ = "usuarios"
    _table_args_ = (
        CheckConstraint(f"rol IN ({lista_sql(ROLES)})", name="ck_usuarios_rol"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    correo: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)