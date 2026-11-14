"""Configuración: lee las variables de entorno del archivo .env (raíz del repositorio)."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]   # carpeta backend/ (este archivo está en backend/src/utils/)
ROOT_DIR = BASE_DIR.parent   # raíz del repositorio
FRONTEND_DIR = ROOT_DIR / "frontend"


class Settings(BaseSettings):
    # Sin valor por defecto a propósito: si falta en .env, la app NO arranca.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = f"sqlite:///{(BASE_DIR / 'mesa_soporte.db').as_posix()}"
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    # Clave de los usuarios FICTICIOS de prueba. Solo la usa seed.py; se define en el .env local.
    DEMO_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def cors_origins_list(self) -> list:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
