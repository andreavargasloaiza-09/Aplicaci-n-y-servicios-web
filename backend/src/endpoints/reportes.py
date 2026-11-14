"""Endpoints de los casos de soporte. Cada uno es delgado: valida permisos y llama a servicios.py."""
from typing import Optional

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from src.services import reportes as servicios
from src.database.connection import get_db
from src.schemas.base import EstadoCaso, GrupoCasos
from src.schemas.intervencion import IntervencionCrear, IntervencionSalida
from src.schemas.reporte import (
    AsignarEntrada,
    CalificarEntrada,
    CerrarEntrada,
    ReporteCrear,
    ReporteDetalle,
    ReporteResumen,
    TerminarEntrada,
)
from src.utils.security import Sesion, obtener_sesion

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.post("", response_model=ReporteDetalle, status_code=201,
             summary="Reportar un caso (CA-01)")
def crear(datos: ReporteCrear, db: Session = Depends(get_db),
          sesion: Sesion = Security(obtener_sesion, scopes=["reportes:crear"])):
    return servicios.crear_reporte(db, sesion, datos)


@router.get("", response_model=list[ReporteResumen],
            summary="Listar casos (cada rol ve los suyos; coordinación todos)")
def listar(estado: Optional[EstadoCaso] = None, grupo: Optional[GrupoCasos] = None,
           db: Session = Depends(get_db), sesion: Sesion = Security(obtener_sesion)):
    return servicios.listar_reportes(db, sesion, estado, grupo)


@router.get("/{reporte_id}", response_model=ReporteDetalle,
            summary="Consultar un caso: estado, responsable, resultado (CA-03, CA-05)")
def detalle(reporte_id: int, db: Session = Depends(get_db),
            sesion: Sesion = Security(obtener_sesion)):
    return servicios.obtener_reporte(db, sesion, reporte_id)


@router.get("/{reporte_id}/historial", response_model=list[IntervencionSalida],
            summary="Historial de intervenciones en orden cronológico (CA-04)")
def historial(reporte_id: int, db: Session = Depends(get_db),
              sesion: Sesion = Security(obtener_sesion)):
    return servicios.historial(db, sesion, reporte_id)


@router.patch("/{reporte_id}/asignar", response_model=ReporteDetalle,
              summary="Asignar técnico (solo coordinación) (CA-02)")
def asignar(reporte_id: int, datos: AsignarEntrada, db: Session = Depends(get_db),
            sesion: Sesion = Security(obtener_sesion, scopes=["reportes:asignar"])):
    return servicios.asignar(db, sesion, reporte_id, datos)


@router.patch("/{reporte_id}/iniciar", response_model=ReporteDetalle,
              summary="Iniciar la reparación (técnico asignado)")
def iniciar(reporte_id: int, db: Session = Depends(get_db),
            sesion: Sesion = Security(obtener_sesion, scopes=["reportes:intervenir"])):
    return servicios.iniciar(db, sesion, reporte_id)


@router.post("/{reporte_id}/intervenciones", response_model=IntervencionSalida, status_code=201,
             summary="Registrar una intervención (técnico asignado)")
def intervenir(reporte_id: int, datos: IntervencionCrear, db: Session = Depends(get_db),
               sesion: Sesion = Security(obtener_sesion, scopes=["reportes:intervenir"])):
    return servicios.registrar_intervencion(db, sesion, reporte_id, datos)


@router.patch("/{reporte_id}/terminar", response_model=ReporteDetalle,
              summary="Terminar la reparación con su respuesta (técnico asignado)")
def terminar(reporte_id: int, datos: TerminarEntrada, db: Session = Depends(get_db),
             sesion: Sesion = Security(obtener_sesion, scopes=["reportes:intervenir"])):
    return servicios.terminar(db, sesion, reporte_id, datos)


@router.patch("/{reporte_id}/cerrar", response_model=ReporteDetalle,
              summary="Cerrar el caso (técnico asignado). No se puede reabrir")
def cerrar(reporte_id: int, datos: CerrarEntrada, db: Session = Depends(get_db),
           sesion: Sesion = Security(obtener_sesion, scopes=["reportes:cerrar"])):
    return servicios.cerrar(db, sesion, reporte_id, datos)


@router.post("/{reporte_id}/calificacion", response_model=ReporteDetalle,
             summary="Calificar un caso cerrado (solicitante)")
def calificar(reporte_id: int, datos: CalificarEntrada, db: Session = Depends(get_db),
              sesion: Sesion = Security(obtener_sesion, scopes=["reportes:calificar"])):
    return servicios.calificar(db, sesion, reporte_id, datos)
