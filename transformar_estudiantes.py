import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA_CSV = BASE_DIR / "datos" / "estudiantes.csv"
RUTA_JSON = BASE_DIR / "salida" / "estudiantes_resumen.json"

# Paso 1 — Verificar Python
print("Hola, Aplicaciones y Servicios Web")

# Paso 3 y 4 — Crear una función de transformación
def transformar_estudiante(estudiante: dict) -> dict:
    """Transforma el diccionario de un estudiante según las reglas del panel académico."""
    

    estado_str = "Activo" if estudiante.get("activo", "").lower() == "true" else "Inactivo"
    
    return {
        "id": estudiante["codigo"],
        "nombre_completo": f"{estudiante['nombre']} {estudiante['apellido']}",
        "semestre": int(estudiante["semestre"]),
        "promedio": float(estudiante["promedio"]),
        "estado": estado_str
    }

# Paso 2 y 5 — Leer el CSV, transformar todos los registros y guardarlos en una lista
estudiantes_transformados = []

try:
    with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo_csv:
        
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            estudiante_modificado = transformar_estudiante(fila)
            estudiantes_transformados.append(estudiante_modificado)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {RUTA_CSV}")
    print("Asegúrate de haber creado la carpeta 'datos' y puesto el archivo 'estudiantes.csv' ahí.")
    exit()

# Paso 6 — Serializar y guardar el JSON
def serializar_estudiantes(ruta: Path, estudiantes: list[dict]) -> None:
    """Serializa una lista de diccionarios Python a un archivo JSON UTF-8."""
    ruta.parent.mkdir(exist_ok=True)
    
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, indent=2, ensure_ascii=False)

serializar_estudiantes(RUTA_JSON, estudiantes_transformados)
print(f"Archivo JSON generado: {RUTA_JSON}")

# Paso 7 — Deserializar el JSON generado
def deserializar_estudiantes(ruta: Path) -> list[dict]:
    """Deserializa un archivo JSON a una lista de diccionarios Python."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)

estudiantes_recuperados = deserializar_estudiantes(RUTA_JSON)

print("\nDatos recuperados desde el JSON:")
if estudiantes_recuperados:
    print(estudiantes_recuperados[0])
print(f"Total recuperado: {len(estudiantes_recuperados)}")