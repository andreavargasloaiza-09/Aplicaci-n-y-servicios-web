"""
Revisa que el proyecto esté completo y bien instalado en ESTE computador.

Uso (desde cualquier carpeta, con el entorno virtual activo):
    python verificar_instalacion.py
"""
import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
problemas = []


def revisar(nombre, ok, ayuda=""):
    print(("  OK     " if ok else "  FALLA  ") + nombre)
    if not ok:
        problemas.append(f"{nombre}. {ayuda}".strip())


print("1) Paquetes de Python")
PAQUETES = [
    ("fastapi", ["fastapi"]), ("uvicorn", ["uvicorn"]), ("sqlalchemy", ["sqlalchemy"]),
    ("pydantic", ["pydantic"]), ("pydantic-settings", ["pydantic_settings"]),
    ("pyjwt", ["jwt"]), ("bcrypt", ["bcrypt"]),
    ("python-multipart", ["python_multipart", "multipart"]), ("jinja2", ["jinja2"]),
]
for paquete, modulos in PAQUETES:
    instalado = any(importlib.util.find_spec(m) is not None for m in modulos)
    revisar(paquete, instalado, "Ejecute pip install -r requirements.txt con el entorno virtual activo")

print("2) Archivo .env (en la raíz del repositorio)")
env = RAIZ / ".env"
texto = env.read_text(encoding="utf-8") if env.exists() else ""
revisar(".env existe", env.exists(), "Copie .env.example como .env")
for clave in ("SECRET_KEY", "DEMO_PASSWORD"):
    m = re.search(rf"^{clave}=(.*)$", texto, re.MULTILINE)
    valor = m.group(1).strip() if m else ""
    revisar(f"{clave} definida", bool(valor) and not valor.startswith("reemplace-por"),
            f"Escriba {clave}=... en el .env (ver .env.example)")

print("3) Código del backend")
patron = re.compile(r"(?<![A-Za-z0-9_])_(file|name|main|all|tablename|table_args|init)_(?![A-Za-z0-9_])")
danados = []
for archivo in sorted((RAIZ / "backend").rglob("*.py")):
    for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
        if patron.search(linea):
            danados.append(f"{archivo.relative_to(RAIZ).as_posix()} (línea {n})")
revisar("sin guiones bajos perdidos (__file__, __tablename__, ...)", not danados,
        "Archivos dañados: " + "; ".join(danados[:6]) + ". Vuelva a copiar el proyecto desde el zip, no desde texto")
paquetes = ["", "database", "endpoints", "entities", "schemas", "services", "utils"]
sin_init = [p or "src" for p in paquetes if not (RAIZ / "backend" / "src" / p / "__init__.py").exists()]
revisar("cada carpeta de src/ tiene su __init__.py", not sin_init, "Falta __init__.py en: " + ", ".join(sin_init))
init_ent = RAIZ / "backend" / "src" / "entities" / "__init__.py"
revisar("src/entities/__init__.py registra las 4 tablas",
        init_ent.exists() and all(t in init_ent.read_text(encoding="utf-8") for t in ("Usuario", "Categoria", "Reporte", "Intervencion")),
        "Ese archivo está vacío o dañado")

print("4) Frontend")
esperados = (["static/css/styles.css"]
             + [f"static/js/{n}.js" for n in ("api", "ui", "login", "solicitante", "tecnico", "coordinador")]
             + [f"templates/{n}.html" for n in ("base", "base_app", "login", "solicitante", "tecnico", "coordinador")])
faltan = [e for e in esperados if not (RAIZ / "frontend" / e).exists()]
revisar("frontend completo (13 archivos)", not faltan, "Faltan: " + ", ".join(faltan[:6]))

print()
if problemas:
    print(f"Se encontraron {len(problemas)} problema(s):")
    for p in problemas:
        print("  -", p)
    sys.exit(1)
print("Todo en orden. Siguiente paso:  cd backend  ->  python seed.py  ->  uvicorn src.main:app --reload")
