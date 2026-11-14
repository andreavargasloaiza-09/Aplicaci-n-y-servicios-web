"""Punto de entrada: crea la aplicación FastAPI (API REST + pantallas web) y registra rutas y errores."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import src.entities  # noqa: F401  (registra las tablas antes de crearlas)
from src.utils.config import FRONTEND_DIR, settings
from src.database.connection import Base, engine
from src.utils.reglas import ErrorDeFlujo
from src.endpoints import auth, catalogos, consolidado, paginas, reportes

logger = logging.getLogger("mesa_soporte")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Mesa de servicios de soporte tecnológico",
    description="API REST para reportar, asignar, atender, cerrar y consultar casos de soporte.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ErrorDeFlujo)
async def manejar_error_de_flujo(_request: Request, exc: ErrorDeFlujo):
    """Acción no válida para el estado actual del caso (por ejemplo, caso cerrado)."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def manejar_error_inesperado(_request: Request, exc: Exception):
    """El detalle técnico queda en el log del servidor; al cliente no se le revela (RNF seguridad)."""
    logger.exception("Error no controlado", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


app.include_router(auth.router)
app.include_router(catalogos.router)
app.include_router(reportes.router)
app.include_router(consolidado.router)

# Frontend: pantallas HTML (plantillas Jinja2) y archivos estáticos (CSS y JavaScript).
app.include_router(paginas.router)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")