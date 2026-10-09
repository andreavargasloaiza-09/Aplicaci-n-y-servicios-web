from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.crud import sensor_magnitud as crud_magnitud
from app.crud import sensor as crud_sensor
from app.schemas.sensor_magnitud import SensorMagnitudResponse

router = APIRouter(tags=["Magnitudes"])

@router.get("/sensores/{id}/magnitudes", response_model=List[SensorMagnitudResponse])
def obtener_magnitudes_de_sensor(id: int, db: Session = Depends(get_db)):
    sensor = crud_sensor.get_sensor_by_id(db, id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return crud_magnitud.get_magnitudes_by_sensor(db, id)

@router.get("/sensor-magnitudes/{id}", response_model=SensorMagnitudResponse)
def obtener_magnitud_por_id(id: int, db: Session = Depends(get_db)):
    magnitud = crud_magnitud.get_magnitud_by_id(db, id)
    if not magnitud:
        raise HTTPException(status_code=404, detail="Magnitud no encontrada")
    return magnitud