from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class MedicionBase(BaseModel):
    estudiante_id: int
    variable: str = Field(..., max_length=50)
    valor: Decimal
    unidad: str = Field(..., max_length=20)
    fecha_hora: datetime

class MedicionCreate(MedicionBase):
    pass

class MedicionUpdate(BaseModel):
    estudiante_id: int | None = None
    variable: str | None = Field(None, max_length=50)
    valor: Decimal | None = None
    unidad: str | None = Field(None, max_length=20)
    fecha_hora: datetime | None = None

class MedicionResponse(MedicionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int