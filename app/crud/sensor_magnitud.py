from sqlalchemy.orm import Session
from app.models.sensor_magnitud import SensorMagnitud

def get_magnitudes_by_sensor(db: Session, sensor_id: int):
    return db.query(SensorMagnitud).filter(SensorMagnitud.sensor_id == sensor_id).all()

def get_magnitud_by_id(db: Session, magnitud_id: int):
    return db.query(SensorMagnitud).filter(SensorMagnitud.id == magnitud_id).first()