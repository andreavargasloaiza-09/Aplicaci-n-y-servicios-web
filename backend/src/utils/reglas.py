"""
Reglas de negocio PURAS: no dependen de FastAPI ni de la base de datos.

Todo lo que define el proceso de soporte vive aquí: roles, estados, transiciones
y permisos (scopes). Si el profesor cambia una regla, se cambia en este archivo.

Origen en el documento de requisitos: RN-03 (ciclo de vida), RN-04 (asignación),
RN-05 (cierre), RN-06 (control de acceso) y RF-07 (casos cerrados bloqueados).
"""
from dataclasses import dataclass


class ErrorDeFlujo(Exception):
    """La acción pedida no es válida para el estado actual del caso (se responde 409)."""


# ----------------------------------------------------------------- roles
ROL_SOLICITANTE = "solicitante"
ROL_TECNICO = "tecnico"
ROL_COORDINADOR = "coordinador"
ROLES = (ROL_SOLICITANTE, ROL_TECNICO, ROL_COORDINADOR)

# ---------------------------------------------------------------- estados (RN-03)
REPORTADO = "reportado"
ASIGNADO = "asignado"
EN_REPARACION = "en_reparacion"
TERMINADO = "terminado"
CERRADO = "cerrado"
ESTADOS = (REPORTADO, ASIGNADO, EN_REPARACION, TERMINADO, CERRADO)
ESTADOS_ABIERTOS = (REPORTADO, ASIGNADO, EN_REPARACION, TERMINADO)

ETIQUETAS_ESTADO = {
    REPORTADO: "Reportado",
    ASIGNADO: "Asignado",
    EN_REPARACION: "En reparación",
    TERMINADO: "Terminado",
    CERRADO: "Cerrado",
}

# ---------------------------------------------------------------- cierre (RN-05)
MOTIVO_RESUELTO = "resuelto"
MOTIVO_ERROR = "error"
MOTIVO_DUPLICADO = "duplicado"
MOTIVOS_CIERRE = (MOTIVO_RESUELTO, MOTIVO_ERROR, MOTIVO_DUPLICADO)
# Casos erróneos o duplicados: se cierran (no se borran) con observación. Como cierra el técnico
# asignado, un caso sin técnico debe asignarse primero.
MOTIVOS_CIERRE_ANTICIPADO = (MOTIVO_ERROR, MOTIVO_DUPLICADO)

TIPOS_CATEGORIA = ("incidente", "solicitud")
TIPOS_INTERVENCION = ("registro", "asignacion", "nota", "estado", "cierre")

# ---------------------------------------------------------------- permisos (RN-06)
# Estos scopes viajan dentro del token JWT. Para cambiar QUIÉN puede hacer algo,
# se mueve el scope de un rol a otro (por ejemplo "reportes:cerrar").
SCOPES_POR_ROL = {
    ROL_SOLICITANTE: [
        "reportes:crear",
        "reportes:leer_propios",
        "reportes:calificar",
    ],
    ROL_TECNICO: [
        "reportes:leer_asignados",
        "reportes:intervenir",   # iniciar, anotar intervenciones y terminar
        "reportes:cerrar",       # cierra el técnico asignado al caso (lo confirmó el profesor)
    ],
    ROL_COORDINADOR: [
        "reportes:leer_todos",
        "reportes:asignar",
        "reportes:consolidado",
        "usuarios:listar",
    ],
}

DESCRIPCION_SCOPES = {
    "reportes:crear": "Reportar un caso de soporte",
    "reportes:leer_propios": "Consultar los casos propios",
    "reportes:calificar": "Calificar un caso propio cerrado",
    "reportes:leer_asignados": "Consultar los casos asignados",
    "reportes:intervenir": "Iniciar, intervenir y terminar casos asignados",
    "reportes:leer_todos": "Consultar todos los casos",
    "reportes:asignar": "Asignar técnico a un caso",
    "reportes:cerrar": "Cerrar los casos asignados",
    "reportes:consolidado": "Ver el consolidado de casos",
    "usuarios:listar": "Listar técnicos",
}


# ---------------------------------------------------------------- transiciones
@dataclass(frozen=True)
class Transicion:
    origenes: tuple   # estados desde los que se permite la acción
    destino: str      # estado al que pasa el caso


TRANSICIONES = {
    "asignar": Transicion(origenes=(REPORTADO,), destino=ASIGNADO),
    "iniciar": Transicion(origenes=(ASIGNADO,), destino=EN_REPARACION),
    "terminar": Transicion(origenes=(EN_REPARACION,), destino=TERMINADO),
    "cerrar": Transicion(origenes=(TERMINADO,), destino=CERRADO),
}

MENSAJE_CASO_CERRADO = (
    "El caso está cerrado: no admite cambios de estado ni nuevas intervenciones."
)


def estado_destino(accion: str, estado_actual: str, motivo: str = None) -> str:
    """Devuelve el estado al que pasa el caso, o lanza ErrorDeFlujo si no es válido."""
    if estado_actual == CERRADO:
        raise ErrorDeFlujo(MENSAJE_CASO_CERRADO)

    transicion = TRANSICIONES[accion]
    origenes = transicion.origenes
    if accion == "cerrar" and motivo in MOTIVOS_CIERRE_ANTICIPADO:
        origenes = ESTADOS_ABIERTOS

    if estado_actual not in origenes:
        raise ErrorDeFlujo(
            f"No se puede ejecutar la acción '{accion}' sobre un caso en estado "
            f"'{ETIQUETAS_ESTADO.get(estado_actual, estado_actual)}'."
        )
    return transicion.destino


def validar_intervencion_permitida(estado_actual: str) -> None:
    """RF-07: un caso cerrado no admite nuevas intervenciones."""
    if estado_actual == CERRADO:
        raise ErrorDeFlujo(MENSAJE_CASO_CERRADO)