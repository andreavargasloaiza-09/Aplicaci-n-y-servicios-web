"""Vista consolidada para coordinación (CA-06, RF-09)."""
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from src.services import reportes as servicios
from src.database.connection import get_db
from src.schemas.consolidado import ConsolidadoSalida
from src.utils.security import Sesion, obtener_sesion

router = APIRouter(prefix="/api/consolidado", tags=["Coordinación"])


@router.get("", response_model=ConsolidadoSalida,
            summary="Casos abiertos y cerrados con estado y responsable")
def ver(db: Session = Depends(get_db),
        sesion: Sesion = Security(obtener_sesion, scopes=["reportes:consolidado"])):
    return servicios.consolidado(db)
