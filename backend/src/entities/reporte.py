"""Entidad Reporte: el caso de soporte."""
from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base
from src.utils.fechas import ahora
from src.utils.reglas import ESTADOS, MOTIVOS_CIERRE, REPORTADO
from src.utils.sql import lista_sql


class Reporte(Base):
    __tablename__ = "reportes"
    __table_args__ = (
        CheckConstraint(f"estado IN ({lista_sql(ESTADOS)})", name="ck_reportes_estado"),
        CheckConstraint(
            f"motivo_cierre IS NULL OR motivo_cierre IN ({lista_sql(MOTIVOS_CIERRE)})",
            name="ck_reportes_motivo_cierre",
        ),
        CheckConstraint(
            "calificacion IS NULL OR (calificacion BETWEEN 1 AND 5)",
            name="ck_reportes_calificacion",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    tecnico_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id"), index=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))

    # Datos del reporte (RN-01)
    descripcion: Mapped[str] = mapped_column(Text)
    placa: Mapped[str] = mapped_column(String(50))
    telefono: Mapped[str] = mapped_column(String(20))
    nombre_solicitante: Mapped[str] = mapped_column(String(120))
    area: Mapped[str] = mapped_column(String(100))

    estado: Mapped[str] = mapped_column(String(20), default=REPORTADO, index=True)

    # Resultado de la atención
    respuesta_tecnica: Mapped[Optional[str]] = mapped_column(Text)
    motivo_cierre: Mapped[Optional[str]] = mapped_column(String(20))
    observacion_cierre: Mapped[Optional[str]] = mapped_column(Text)

    # Encuesta de satisfacción (RF-11)
    calificacion: Mapped[Optional[int]] = mapped_column(Integer)
    comentario_calificacion: Mapped[Optional[str]] = mapped_column(Text)

    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    cerrado_en: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    solicitante: Mapped["Usuario"] = relationship(foreign_keys="Reporte.solicitante_id")
    tecnico: Mapped[Optional["Usuario"]] = relationship(foreign_keys="Reporte.tecnico_id")
    categoria: Mapped["Categoria"] = relationship()
    intervenciones: Mapped[list["Intervencion"]] = relationship(
        back_populates="reporte", order_by="Intervencion.id"
    )
