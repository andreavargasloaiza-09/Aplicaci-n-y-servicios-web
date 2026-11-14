"""Listas de apoyo para la interfaz: categorías y técnicos disponibles."""
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from src.services import catalogos as servicios
from src.database.connection import get_db
from src.schemas.categoria import CategoriaSalida
from src.schemas.usuario import UsuarioSalida
from src.utils.security import Sesion, obtener_sesion

router = APIRouter(prefix="/api", tags=["Catálogos"])


@router.get("/categorias", response_model=list[CategoriaSalida], summary="Listar categorías")
def categorias(db: Session = Depends(get_db), sesion: Sesion = Security(obtener_sesion)):
    return servicios.listar_categorias(db)


@router.get("/usuarios/tecnicos", response_model=list[UsuarioSalida],
            summary="Listar técnicos (solo coordinación)")
def tecnicos(db: Session = Depends(get_db),
             sesion: Sesion = Security(obtener_sesion, scopes=["usuarios:listar"])):
    return servicios.listar_tecnicos(db)