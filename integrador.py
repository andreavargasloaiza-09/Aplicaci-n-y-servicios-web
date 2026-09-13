import csv
import json
from datetime import datetime
import os
from endpoint import enviar_mediciones, consultar_resultados

#PUNTO 7: INTEGRACIÓN HTTP
URL_BASE = "https://appsweb.quantaiot.co"
ID_EQUIPO = "EQUIPO-11-APPSWEB" 

#1. FUNCIONES DE CARGA DE DATOS
def cargar_datos():
    datos_a = []
    datos_b = []
    
    # 1. Cargar Proveedor A (JSON)
    try:
        with open("datos/proveedor_a.json", "r", encoding="utf-8") as f_a:
            contenido = json.load(f_a)
            datos_a = contenido.get("records", [])
    except FileNotFoundError:
        print("[Error Controlado] No se encontró el archivo datos/proveedor_a.json.")
    except json.JSONDecodeError:
        print("[Error Controlado] El archivo proveedor_a.json no tiene un formato JSON válido.")
        
    # 2. Cargar Proveedor B (CSV)
    try:
        with open("datos/proveedor_b.csv", "r", encoding="utf-8") as f_b:
            reader_b = csv.reader(f_b, delimiter=";")
            next(reader_b, None)
            datos_b = list(reader_b)
    except FileNotFoundError:
        print("[Error Controlado] No se encontró el archivo datos/proveedor_b.csv.")
    except Exception as e:
        print(f"[Error Controlado] Ocurrió un error al leer el CSV: {e}")

    return datos_a, datos_b


#2. FUNCIONES DE NORMALIZACIÓN (PUNTO 3 & 5)
# Normalización de datos del Proveedor A y B
def normalizar_a(registro):
    try:

        temp_f_raw = registro.get("measurements", {}).get("temperature_f")
        temp_f = float(temp_f_raw)
        temp_c = (temp_f - 32) * 5 / 9

        vien_ms_raw = registro.get("measurements", {}).get("wind_speed_ms")
        vien_ms = float(vien_ms_raw)
        vien_kmh = vien_ms * 3.6

        id_registro = str(registro.get("provider_record_id", "desconocido")).strip()

        registro_normalizado = {
            "ciudad": registro.get("station", {}).get("city_name", "").strip(),
            "pais": registro.get("station", {}).get("country_code", "").strip(),
            "latitud": float(registro.get("location", {}).get("lat")),
            "longitud": float(registro.get("location", {}).get("lon")),
            "temperatura_c": temp_c,
            "humedad": float(registro.get("measurements", {}).get("relative_humidity")),
            "viento_kmh": vien_kmh,
            "fecha_hora": registro.get("observed_at", "").strip(),
            "origen": "proveedor_a", 
        }
        return registro_normalizado, id_registro, None 

    except Exception as e:
        id_registro = str(registro.get("provider_record_id", "desconocido")).strip()
        return None, id_registro, f"Error normalización: {str(e)}"


def normalizar_b(fila_csv):

    try:

        id_registro = str(fila_csv[0]).strip() if fila_csv else "desconocido"

        # 1. Parsear fecha (DD/MM/YYYY HH:mm -> ISO)
        fecha_obj = datetime.strptime(fila_csv[8].strip(), "%d/%m/%Y %H:%M")
        fecha_iso = fecha_obj.isoformat()

        # 2. Construir objeto según Contrato API
        registro_normalizado = {
            "ciudad": fila_csv[1].strip(),
            "pais": fila_csv[2].strip(),
            "latitud": float(fila_csv[3]),
            "longitud": float(fila_csv[4]),
            "temperatura_c": float(fila_csv[5]),
            "humedad": float(fila_csv[6]),
            "viento_kmh": float(fila_csv[7]),
            "fecha_hora": fecha_iso,
            "origen": "proveedor_b", 
        }
        return registro_normalizado, id_registro, None  

    except Exception as e:
        # Si falla cualquier casting (float, fecha, etc.), se atrapa el error
        id_registro = str(fila_csv[0]).strip()
        return None, id_registro, f"Error normalización: {str(e)}"


#FUNCIONES DE VALIDACIÓN (PUNTO 4)
def validar_registro(registro):
    # Validar campos no vacíos
    if not registro["ciudad"] or not registro["pais"]:
        return False, "Ciudad o país vacíos"

    # Validar rangos geográficos
    if not (-90 <= registro["latitud"] <= 90):
        return False, f"Latitud fuera de rango: {registro['latitud']}"

    if not (-180 <= registro["longitud"] <= 180):
        return False, f"Longitud fuera de rango: {registro['longitud']}"

    # Validar rangos meteorológicos
    if not (0 <= registro["humedad"] <= 100):
        return False, f"Humedad fuera de rango: {registro['humedad']}"

    if registro["viento_kmh"] < 0:
        return False, f"Viento negativo: {registro['viento_kmh']}"

    return True, None


#5. FLUJO PRINCIPAL (__main__)

if __name__ == "__main__":

    #PUNTO 2: CARGA DE DATOS
    datos_a, datos_b = cargar_datos()

    #PUNTO 3: NORMALIZACIÓN
    registros_normalizados = []
    errores_normalizacion = []

    # Normalizar registros del Proveedor A
    for reg in datos_a:
        resultado, id_registro, error = normalizar_a(reg)
        if resultado:
            registros_normalizados.append(resultado)
        else:
            errores_normalizacion.append({"id_registro": id_registro, "error": error})

    # Normalizar registros del Proveedor B
    for fila in datos_b:
        resultado, id_registro, error = normalizar_b(fila)
        if resultado:
            registros_normalizados.append(resultado)
        else:
            errores_normalizacion.append({"id_registro": id_registro, "error": error})

    # Guardar en salida/normalizadas.json
    os.makedirs("salida", exist_ok=True)
    with open("salida/normalizadas.json", "w", encoding="utf-8") as f:
        json.dump(registros_normalizados, f, indent=2, ensure_ascii=False)

    #PUNTO 4: VALIDACIÓN LOCAL
    registros_validos = []
    rechazados_localmente = []

    for reg in registros_normalizados:
        es_valido, motivo = validar_registro(reg)
        if es_valido:
            registros_validos.append(reg)
        else:
            rechazados_localmente.append({"registro": reg, "motivo": motivo})


if __name__ == "__main__":
    exitosos, fallidos = enviar_mediciones(registros_validos, URL_BASE, ID_EQUIPO)
    print(f"Punto 7 completado: {len(exitosos)} aceptados | {len(fallidos)} fallidos")

    if fallidos:
        print("Respuesta de la API para el primer fallo:", fallidos[0])

    print("\n[Punto 9] Consultando estado final de las mediciones en el servidor...")
    resultado_auditoria = consultar_resultados(URL_BASE, ID_EQUIPO)
    
    if resultado_auditoria["estado"] == "EXITO":
        print(f"Auditoría exitosa. Registros encontrados en el servidor: {len(resultado_auditoria['datos'])}")
        with open("salida/auditoria_servidor.json", "w", encoding="utf-8") as f:
            json.dump(resultado_auditoria['datos'], f, indent=4, ensure_ascii=False)
    else:
        print(f"Advertencia en la auditoría: {resultado_auditoria['detalle']}")

    #10. GENERACIÓN DEL REPORTE FINAL
    reporte_final = {
        "estadisticas": {
            "total_registros_procesados": len(datos_a) + len(datos_b),
            "proveedor_a_procesados": len(datos_a),
            "proveedor_b_procesados": len(datos_b),
            "validos_localmente": len(registros_validos),
            "rechazados_localmente": len(rechazados_localmente),
            "exitosos_en_api": len(exitosos),
            "fallidos_en_api": len(fallidos)
        },
        "detalle_rechazados_localmente": rechazados_localmente,
        "detalle_fallios_api": fallidos
    }

    os.makedirs("salida", exist_ok=True)
    with open("salida/reporte.json", "w", encoding="utf-8") as f:
        json.dump(reporte_final, f, indent=4, ensure_ascii=False)

    print("\n[Punto 10] Reporte generado exitosamente en: salida/reporte.json")