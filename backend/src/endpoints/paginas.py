"""
Pantallas web, renderizadas con Jinja2: el frontend también es parte de la aplicación FastAPI.

Estas rutas solo entregan la estructura HTML de cada pantalla. Los DATOS no se leen aquí:
el JavaScript de la página los pide a la API REST (/api/...) con el token del usuario, y es la API
quien verifica los permisos. Por eso estas rutas no consultan la base de datos.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.utils.config import FRONTEND_DIR
from src.utils.reglas import ETIQUETAS_ESTADO

templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# include_in_schema=False: las pantallas no aparecen en /docs (ahí solo va la API).
router = APIRouter(tags=["Pantallas"], include_in_schema=False)


def _pantalla(request: Request, plantilla: str):
    # La lista de estados sale de reglas.py, así los filtros no se escriben dos veces.
    return templates.TemplateResponse(
        request=request, name=plantilla, context={"estados": ETIQUETAS_ESTADO}
    )


@router.get("/", response_class=HTMLResponse)
def ingreso(request: Request):
    return _pantalla(request, "login.html")


@router.get("/solicitante", response_class=HTMLResponse)
def pantalla_solicitante(request: Request):
    return _pantalla(request, "solicitante.html")


@router.get("/tecnico", response_class=HTMLResponse)
def pantalla_tecnico(request: Request):
    return _pantalla(request, "tecnico.html")


@router.get("/coordinador", response_class=HTMLResponse)
def pantalla_coordinador(request: Request):
    return _pantalla(request, "coordinador.html")
