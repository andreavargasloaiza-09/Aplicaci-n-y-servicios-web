from sqlalchemy.orm import Session
from app.models.sensor_magnitud import SensorMagnitud

def get_magnitudes_by_sensor(db: Session, sensor_id: int):
    return db.query(SensorMagnitud).filter(SensorMagnitud.sensor_id == sensor_id).all()

def get_magnitud_by_id(db: Session, magnitud_id: int):
    return db.query(SensorMagnitud).filter(SensorMagnitud.id == magnitud_id).first()

def get_sensor_magnitud_by_sensor_and_nombre(db: Session, sensor_id: int, magnitud_nombre: str):
    return db.query(SensorMagnitud).filter(
        SensorMagnitud.sensor_id == sensor_id,
        SensorMagnitud.magnitud == magnitud_nombre
    ).first()