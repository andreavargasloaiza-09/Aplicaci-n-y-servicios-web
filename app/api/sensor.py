from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.crud import sensor as crud_sensor
from app.schemas.sensor import SensorResponse

router = APIRouter(tags=["Sensores"])

@router.get("/sensores", response_model=List[SensorResponse])
def obtener_sensores(db: Session = Depends(get_db)):
    return crud_sensor.get_sensores(db)

@router.get("/sensores/{id}", response_model=SensorResponse)
def obtener_sensor_por_id(id: int, db: Session = Depends(get_db)):
    sensor = crud_sensor.get_sensor_by_id(db, id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.get("/sensores/por-codigo/{codigo}", response_model=SensorResponse)
def obtener_sensor_por_codigo(codigo: str, db: Session = Depends(get_db)):
    sensor = crud_sensor.get_sensor_by_codigo(db, codigo)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor