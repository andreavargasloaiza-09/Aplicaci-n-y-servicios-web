"""
Lógica de los casos de soporte: aplica las reglas de reglas.py, guarda en la base de datos
y deja cada actuación en el historial (CA-04). Cada operación hace UN solo commit,
así el cambio de estado y su entrada de historial se guardan juntos o no se guardan.
"""
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from src.entities.categoria import Categoria
from src.entities.intervencion import Intervencion
from src.entities.reporte import Reporte
from src.entities.usuario import Usuario
from src.schemas.intervencion import IntervencionCrear
from src.schemas.reporte import (
    AsignarEntrada,
    CalificarEntrada,
    CerrarEntrada,
    ReporteCrear,
    TerminarEntrada,
)
from src.utils import reglas
from src.utils.fechas import ahora
from src.utils.security import Sesion


# ------------------------------------------------------------------ ayudas internas
def _opciones_resumen():
    return (
        joinedload(Reporte.solicitante),
        joinedload(Reporte.tecnico),
        joinedload(Reporte.categoria),
    )


def _opciones_detalle():
    return _opciones_resumen() + (
        selectinload(Reporte.intervenciones).joinedload(Intervencion.autor),
    )


def _cargar_reporte(db: Session, reporte_id: int) -> Reporte:
    reporte = db.execute(
        select(Reporte).options(*_opciones_detalle()).where(Reporte.id == reporte_id)
    ).scalar_one_or_none()
    if reporte is None:
        raise HTTPException(status_code=404, detail="El caso solicitado no existe")
    return reporte


def _puede_ver(reporte: Reporte, sesion: Sesion) -> bool:
    s, uid = sesion.scopes, sesion.usuario.id
    return (
        "reportes:leer_todos" in s
        or ("reportes:leer_propios" in s and reporte.solicitante_id == uid)
        or ("reportes:leer_asignados" in s and reporte.tecnico_id == uid)
    )


def _exigir_tecnico_asignado(reporte: Reporte, sesion: Sesion) -> None:
    if reporte.tecnico_id != sesion.usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Solo el técnico asignado a este caso puede realizar esta acción",
        )


def _anotar(db, reporte, autor, tipo, descripcion, estado_anterior=None, estado_nuevo=None):
    intervencion = Intervencion(
        reporte=reporte,
        autor_id=autor.id,
        tipo=tipo,
        descripcion=descripcion,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,
    )
    db.add(intervencion)
    return intervencion


# ------------------------------------------------------------------ consultas
def listar_reportes(
    db: Session, sesion: Sesion, estado: Optional[str] = None, grupo: Optional[str] = None
):
    """Cada rol ve solo lo suyo: solicitante sus casos, técnico los asignados, coordinación todos."""
    consulta = select(Reporte).options(*_opciones_resumen())
    if "reportes:leer_todos" not in sesion.scopes:
        filtros = []
        if "reportes:leer_propios" in sesion.scopes:
            filtros.append(Reporte.solicitante_id == sesion.usuario.id)
        if "reportes:leer_asignados" in sesion.scopes:
            filtros.append(Reporte.tecnico_id == sesion.usuario.id)
        if not filtros:
            raise HTTPException(status_code=403, detail="No tiene permisos para esta operación")
        consulta = consulta.where(or_(*filtros))
    if estado:
        consulta = consulta.where(Reporte.estado == estado)
    if grupo == "abiertos":
        consulta = consulta.where(Reporte.estado != reglas.CERRADO)
    elif grupo == "cerrados":
        consulta = consulta.where(Reporte.estado == reglas.CERRADO)
    return db.execute(consulta.order_by(Reporte.id.desc())).scalars().all()


def obtener_reporte(db: Session, sesion: Sesion, reporte_id: int) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    if not _puede_ver(reporte, sesion):
        raise HTTPException(status_code=403, detail="No tiene permiso para ver este caso")
    return reporte


def historial(db: Session, sesion: Sesion, reporte_id: int):
    return obtener_reporte(db, sesion, reporte_id).intervenciones


def consolidado(db: Session) -> dict:
    """CA-06: casos abiertos y cerrados con su estado y responsable."""
    reportes = db.execute(
        select(Reporte).options(*_opciones_resumen()).order_by(Reporte.id.desc())
    ).scalars().all()
    por_estado = {estado: 0 for estado in reglas.ESTADOS}
    for r in reportes:
        por_estado[r.estado] += 1
    abiertos = [r for r in reportes if r.estado != reglas.CERRADO]
    cerrados = [r for r in reportes if r.estado == reglas.CERRADO]
    return {
        "total": len(reportes),
        "abiertos": len(abiertos),
        "cerrados": len(cerrados),
        "por_estado": por_estado,
        "casos_abiertos": abiertos,
        "casos_cerrados": cerrados,
    }


# ------------------------------------------------------------------ acciones sobre el caso
def crear_reporte(db: Session, sesion: Sesion, datos: ReporteCrear) -> Reporte:
    if db.get(Categoria, datos.categoria_id) is None:
        raise HTTPException(status_code=422, detail="La categoría indicada no existe")
    reporte = Reporte(
        solicitante_id=sesion.usuario.id,
        categoria_id=datos.categoria_id,
        descripcion=datos.descripcion,
        placa=datos.placa,
        telefono=datos.telefono,
        nombre_solicitante=datos.nombre_solicitante,
        area=datos.area,
        estado=reglas.REPORTADO,
    )
    db.add(reporte)
    db.flush()   # para obtener el id antes de anotar el historial
    _anotar(db, reporte, sesion.usuario, "registro", "Caso reportado", None, reglas.REPORTADO)
    db.commit()
    return _cargar_reporte(db, reporte.id)


def asignar(db: Session, sesion: Sesion, reporte_id: int, datos: AsignarEntrada) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    destino = reglas.estado_destino("asignar", reporte.estado)
    tecnico = db.get(Usuario, datos.tecnico_id)
    if tecnico is None or tecnico.rol != reglas.ROL_TECNICO or not tecnico.activo:
        raise HTTPException(status_code=422, detail="El usuario indicado no es un técnico válido")
    anterior = reporte.estado
    reporte.tecnico_id = tecnico.id
    reporte.estado = destino
    reporte.actualizado_en = ahora()
    _anotar(db, reporte, sesion.usuario, "asignacion",
            f"Caso asignado al técnico {tecnico.nombre}", anterior, destino)
    db.commit()
    return _cargar_reporte(db, reporte_id)


def iniciar(db: Session, sesion: Sesion, reporte_id: int) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    _exigir_tecnico_asignado(reporte, sesion)
    destino = reglas.estado_destino("iniciar", reporte.estado)
    anterior = reporte.estado
    reporte.estado = destino
    reporte.actualizado_en = ahora()
    _anotar(db, reporte, sesion.usuario, "estado", "El técnico inició la reparación", anterior, destino)
    db.commit()
    return _cargar_reporte(db, reporte_id)


def registrar_intervencion(
    db: Session, sesion: Sesion, reporte_id: int, datos: IntervencionCrear
) -> Intervencion:
    reporte = _cargar_reporte(db, reporte_id)
    _exigir_tecnico_asignado(reporte, sesion)
    reglas.validar_intervencion_permitida(reporte.estado)
    intervencion = _anotar(db, reporte, sesion.usuario, "nota", datos.descripcion)
    reporte.actualizado_en = ahora()
    db.commit()
    db.refresh(intervencion)
    return intervencion


def terminar(db: Session, sesion: Sesion, reporte_id: int, datos: TerminarEntrada) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    _exigir_tecnico_asignado(reporte, sesion)
    destino = reglas.estado_destino("terminar", reporte.estado)
    anterior = reporte.estado
    reporte.estado = destino
    reporte.respuesta_tecnica = datos.respuesta
    reporte.actualizado_en = ahora()
    _anotar(db, reporte, sesion.usuario, "estado",
            f"Reparación terminada. Respuesta al solicitante: {datos.respuesta}", anterior, destino)
    db.commit()
    return _cargar_reporte(db, reporte_id)


def cerrar(db: Session, sesion: Sesion, reporte_id: int, datos: CerrarEntrada) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    # Cierra el técnico asignado al caso (regla confirmada por el profesor).
    _exigir_tecnico_asignado(reporte, sesion)
    destino = reglas.estado_destino("cerrar", reporte.estado, datos.motivo)
    anterior = reporte.estado
    momento = ahora()
    reporte.estado = destino
    reporte.motivo_cierre = datos.motivo
    reporte.observacion_cierre = datos.observacion
    reporte.cerrado_en = momento
    reporte.actualizado_en = momento
    _anotar(db, reporte, sesion.usuario, "cierre",
            f"Caso cerrado ({datos.motivo}). Observación: {datos.observacion}", anterior, destino)
    db.commit()
    return _cargar_reporte(db, reporte_id)


def calificar(db: Session, sesion: Sesion, reporte_id: int, datos: CalificarEntrada) -> Reporte:
    reporte = _cargar_reporte(db, reporte_id)
    if reporte.solicitante_id != sesion.usuario.id:
        raise HTTPException(status_code=403, detail="Solo el solicitante del caso puede calificarlo")
    if reporte.estado != reglas.CERRADO:
        raise reglas.ErrorDeFlujo("La calificación solo se habilita cuando el caso está cerrado")
    if reporte.calificacion is not None:
        raise HTTPException(status_code=409, detail="Este caso ya fue calificado")
    reporte.calificacion = datos.puntuacion
    reporte.comentario_calificacion = datos.comentario
    db.commit()
    return _cargar_reporte(db, reporte_id)
