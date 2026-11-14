"""Entidad Intervencion: historial del caso (notas del técnico y eventos de gestión)."""
from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base
from src.utils.fechas import ahora
from src.utils.reglas import TIPOS_INTERVENCION
from src.utils.sql import lista_sql


class Intervencion(Base):
    __tablename__ = "intervenciones"
    __table_args__ = (
        CheckConstraint(
            f"tipo IN ({lista_sql(TIPOS_INTERVENCION)})", name="ck_intervenciones_tipo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), index=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    descripcion: Mapped[str] = mapped_column(Text)
    estado_anterior: Mapped[Optional[str]] = mapped_column(String(20))
    estado_nuevo: Mapped[Optional[str]] = mapped_column(String(20))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)

    reporte: Mapped["Reporte"] = relationship(back_populates="intervenciones")
    autor: Mapped["Usuario"] = relationship()
