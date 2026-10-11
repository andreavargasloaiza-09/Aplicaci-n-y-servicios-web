from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models.medicion import Medicion
from app.models.sensor_magnitud import SensorMagnitud

def get_mediciones_historicas(
    db: Session, 
    sensor_id: int, 
    desde: Optional[datetime] = None, 
    hasta: Optional[datetime] = None, 
    magnitud: Optional[str] = None, 
    limit: int = 100
):
    # Unir las tablas para filtrar por el id del sensor
    query = db.query(Medicion).join(SensorMagnitud).filter(SensorMagnitud.sensor_id == sensor_id)
    
    # Aplicar filtros si el usuario los proporciona
    if magnitud:
        query = query.filter(SensorMagnitud.magnitud == magnitud)
    if desde:
        query = query.filter(Medicion.timestamp_utc >= desde)
    if hasta:
        query = query.filter(Medicion.timestamp_utc <= hasta)
        
    # Ordenar por fecha descendente y limitar la cantidad
    return query.order_by(Medicion.timestamp_utc.desc()).limit(limit).all()

def get_medicion_by_id(db: Session, medicion_id: int):
    return db.query(Medicion).filter(Medicion.id == medicion_id).first()

def get_ultima_medicion(db: Session, sensor_id: int):
    return db.query(Medicion).join(SensorMagnitud).filter(
        SensorMagnitud.sensor_id == sensor_id
    ).order_by(Medicion.timestamp_utc.desc()).first()

def create_medicion(db: Session, sensor_magnitud_id: int, valor: float, timestamp_utc: datetime):
    db_medicion = Medicion(
        sensor_magnitud_id=sensor_magnitud_id,
        valor=valor,
        timestamp_utc=timestamp_utc
    )
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion