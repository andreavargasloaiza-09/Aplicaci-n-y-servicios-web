"""Conexión a la base de datos (SQLAlchemy). Cambiar de motor = cambiar DATABASE_URL en .env."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.utils.config import settings

_es_sqlite = settings.DATABASE_URL.startswith("sqlite")
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if _es_sqlite else {},
)

if _es_sqlite:
    # SQLite no hace cumplir las claves foráneas si no se activa (integridad referencial, RNF-02).
    @event.listens_for(engine, "connect")
    def _activar_claves_foraneas(conexion, _registro):
        cursor = conexion.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependencia de FastAPI: una sesión por solicitud, siempre se cierra."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()