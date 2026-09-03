import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def transformar_estudiantes(lector):
    estudiantes_transformados = []

    # Paso 3: Transformar cada estudiante
    # (Aquí se cumple el PASO 2 del taller: cada 'fila' es un diccionario Python)
    for fila in lector:
        # Normalizar el valor booleano para el estado
        es_activo = fila["activo"].strip().lower() == "true"

        # Transformación al formato requerido
        estudiante = {
            "id": fila["codigo"],
            "nombre_completo": f"{fila['nombre']} {fila['apellido']}",
            "semestre": int(fila["semestre"]),
            "promedio": float(fila["promedio"]),
            "estado": "Activo" if es_activo else "Inactivo",
        }

        estudiantes_transformados.append(estudiante)

    return estudiantes_transformados


# Abrir el archivo CSV y procesar los datos
ruta_csv = "datos/estudiantes.csv"

# PASO 1: Leer estudiantes.csv con csv.DictReader
with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    # PASO 2 y 3: Se procesa y transforma
    resultado = transformar_estudiantes(lector)

def serializar_estudiantes(ruta: Path, estudiantes: list[dict]) -> None:
    """Serializa una lista de diccionarios Python a un archivo JSON UTF-8."""
    ruta.parent.mkdir(exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, indent=2, ensure_ascii=False)


RUTA_JSON = BASE_DIR / "salida" / "estudiantes_resumen.json"

serializar_estudiantes(RUTA_JSON, resultado)
print(f"Archivo JSON generado: {RUTA_JSON}")

def deserializar_estudiantes(ruta: Path) -> list[dict]:
    """Deserializa un archivo JSON a una lista de diccionarios Python."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)

estudiantes_recuperados = deserializar_estudiantes(RUTA_JSON)

print("\nDatos recuperados desde el JSON:")
print(estudiantes_recuperados[0])
print(f"Total recuperado: {len(estudiantes_recuperados)}")

