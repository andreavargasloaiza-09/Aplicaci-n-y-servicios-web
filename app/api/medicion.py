from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.connection import get_db
from app.models.sensor import Sensor
from app.schemas.medicion import MedicionResponse
from app.crud import medicion as crud_medicion

router = APIRouter()

@router.get("/sensores/{id}/mediciones", response_model=List[MedicionResponse])
def obtener_mediciones_historicas(
    id: int, 
    desde: Optional[datetime] = None, 
    hasta: Optional[datetime] = None, 
    magnitud: Optional[str] = None, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # 1. Validaciones HTTP
    sensor = db.query(Sensor).filter(Sensor.id == id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
    if desde and hasta and desde > hasta:
        raise HTTPException(status_code=400, detail="La fecha 'desde' no puede ser mayor a 'hasta'")

    # 2. Llamado a la capa CRUD
    mediciones = crud_medicion.get_mediciones_historicas(
        db=db, 
        sensor_id=id, 
        desde=desde, 
        hasta=hasta, 
        magnitud=magnitud, 
        limit=limit
    )
    
    return mediciones

from app.crud import sensor as crud_sensor

@router.get("/mediciones/{id}", response_model=MedicionResponse)
def obtener_medicion(id: int, db: Session = Depends(get_db)):
    medicion = crud_medicion.get_medicion_by_id(db, id)
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return medicion

@router.get("/sensores/{id}/ultima-medicion", response_model=MedicionResponse)
def obtener_ultima_medicion(id: int, db: Session = Depends(get_db)):
    # Primero verificamos si el sensor existe para dar un error adecuado
    sensor = crud_sensor.get_sensor_by_id(db, id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
    medicion = crud_medicion.get_ultima_medicion(db, id)
    if not medicion:
        raise HTTPException(status_code=404, detail="El sensor no tiene mediciones registradas")
    return medicion