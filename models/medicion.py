from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Medicion(Base):
    __tablename__ = "mediciones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    variable: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    unidad: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)