from pydantic import BaseModel
from datetime import datetime

class SensorResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    categoria: str
    ubicacion: str
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True