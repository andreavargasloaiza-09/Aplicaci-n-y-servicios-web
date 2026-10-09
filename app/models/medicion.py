from sqlalchemy import Column, Integer, BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class Medicion(Base):
    __tablename__ = "mediciones"
    id = Column(BigInteger, primary_key=True, index=True)
    sensor_magnitud_id = Column(Integer, ForeignKey("sensor_magnitudes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    valor = Column(Numeric(12, 4), nullable=False)
    timestamp_utc = Column(DateTime(timezone=True), nullable=False, index=True)
    fecha_recepcion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    sensor_magnitud = relationship("SensorMagnitud", back_populates="mediciones")