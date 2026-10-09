from sqlalchemy.orm import Session
from app.models.sensor import Sensor

def get_sensores(db: Session):
    return db.query(Sensor).all()

def get_sensor_by_id(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()

def get_sensor_by_codigo(db: Session, codigo: str):
    return db.query(Sensor).filter(Sensor.codigo == codigo).first()