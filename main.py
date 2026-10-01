from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.estudiantes import router as estudiantes_router
from api.mediciones import router as mediciones_router  # 1. Agrega esta importación
from database import SessionLocal

app = FastAPI(title="API de estudiantes")
app.include_router(estudiantes_router)
app.include_router(mediciones_router)  # 2. Registra el router aquí

@app.get("/")
def read_root():
    return {"message": "API de estudiantes conectada a PostgreSQL"}

@app.get("/health/db")
def health_db():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except SQLAlchemyError as exc:
        return {"database": "unavailable", "detail": str(exc)}
