from pydantic import BaseModel

class SensorMagnitudResponse(BaseModel):
    id: int
    sensor_id: int
    magnitud: str
    unidad: str
    valor_minimo: float
    valor_maximo: float

    class Config:
        from_attributes = True