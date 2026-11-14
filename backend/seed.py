"""
Crea las tablas y carga datos FICTICIOS de prueba.

Requiere DEMO_PASSWORD en el .env (clave de prueba para los usuarios ficticios).

Uso (desde la carpeta backend/, con el entorno virtual activo y el .env creado):
    python seed.py            # crea lo que falte
    python seed.py --reset    # BORRA todo y vuelve a crear
"""
import sys

from sqlalchemy import select

import src.entities  # noqa: F401  (registra las tablas)
from src.utils.config import settings
from src.database.connection import Base, SessionLocal, engine
from src.entities.categoria import Categoria
from src.entities.usuario import Usuario
from src.utils.security import hashear_password

USUARIOS = [
    ("Marta Gómez", "coordinador@demo.test", "coordinador"),
    ("Luis Pérez", "tecnico1@demo.test", "tecnico"),
    ("Ana Torres", "tecnico2@demo.test", "tecnico"),
    ("Pedro Ruiz", "solicitante1@demo.test", "solicitante"),
    ("Laura Díaz", "solicitante2@demo.test", "solicitante"),
]

# Categorías de EJEMPLO (la guía pide que el equipo las defina). Ajustar a las que se aprueben.
CATEGORIAS = [
    ("Falla de computador o periférico", "incidente"),
    ("Falla de conectividad o red", "incidente"),
    ("Falla de software o aplicación", "incidente"),
    ("Problema de acceso a plataforma institucional", "incidente"),
    ("Instalación o actualización de software", "solicitud"),
    ("Solicitud de acceso o permisos", "solicitud"),
    ("Préstamo o configuración de equipo", "solicitud"),
]


def main() -> None:
    if not settings.DEMO_PASSWORD:
        sys.exit("Falta DEMO_PASSWORD en el archivo .env (clave de prueba para los usuarios ficticios).")
    if "--reset" in sys.argv:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    hash_demo = hashear_password(settings.DEMO_PASSWORD)
    with SessionLocal() as db:
        for nombre, correo, rol in USUARIOS:
            existe = db.execute(select(Usuario).where(Usuario.correo == correo)).scalar_one_or_none()
            if existe is None:
                db.add(Usuario(nombre=nombre, correo=correo, rol=rol, password_hash=hash_demo))
        for nombre, tipo in CATEGORIAS:
            existe = db.execute(select(Categoria).where(Categoria.nombre == nombre)).scalar_one_or_none()
            if existe is None:
                db.add(Categoria(nombre=nombre, tipo=tipo))
        db.commit()

    print("Base de datos lista.")
    print("Usuarios de prueba (todos usan la clave DEMO_PASSWORD de su .env):")
    for nombre, correo, rol in USUARIOS:
        print(f"  - {rol:<12} {correo}")


if __name__ == "__main__":
    main()