from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict
import zoneinfo

class MeasurementValue(BaseModel):
    value: float
    unit: str

class MQTTPayload(BaseModel):
    sensor_id: str
    timestamp: datetime
    measurements: Dict[str, MeasurementValue]

class MedicionResponse(BaseModel):
    id: int
    sensor_magnitud_id: int
    valor: float
    timestamp_local: datetime 
    
    class Config:
        orm_mode = True

    # Convertidor de UTC a local
    @classmethod
    def from_orm(cls, obj):
        colombia_tz = zoneinfo.ZoneInfo("America/Bogota")
        local_time = obj.timestamp_utc.astimezone(colombia_tz) if obj.timestamp_utc else None
        return cls(
            id=obj.id,
            sensor_magnitud_id=obj.sensor_magnitud_id,
            valor=float(obj.valor),
            timestamp_local=local_time
        )