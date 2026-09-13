import requests
import time

def enviar_mediciones(registros_validos, url_base, id_equipo):
    """
    Envia cada registro valido a la API institucional según el CONTRATO_API.md
    Incluye lógica de reintentos (Punto 8) para errores 5xx y fallos de red.
    """
    endpoint = f"{url_base.rstrip('/')}/api/v1/mediciones"

    headers = {
        "Content-Type": "application/json",
        "X-Equipo": id_equipo
    }

    exitosos = []
    fallidos = []
    max_intentos = 3

    for reg in registros_validos:
        enviado_con_exito = False
        
        for intento in range(1, max_intentos + 1):
            try:
                response = requests.post(endpoint, json=reg, headers=headers, timeout=10)

                # 1. Si es éxito (200 o 201), guardamos y salimos del ciclo de reintentos
                if response.status_code in [200, 201]:
                    exitosos.append(reg)
                    enviado_con_exito = True
                    break
                
                # 2. Si es un error 4xx (del cliente), NO se reintenta porque el dato es erróneo
                elif 400 <= response.status_code < 500:
                    fallidos.append({
                        "registro": reg,
                        "status_code": response.status_code,
                        "respuesta": response.text,
                        "motivo": "Error 4xx (No reintentable)"
                    })
                    enviado_con_exito = True # Marcamos como procesado (fallido definitivo)
                    break
                
                # 3. Si es un error 5xx (del servidor), lanzamos excepción para forzar el reintento
                else:
                    response.raise_for_status()

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
                # Si aún nos quedan intentos, esperamos y reintentamos
                if intento < max_intentos:
                    time.sleep(2 * intento) # Espera progresiva (2s, 4s)
                    continue
                else:
                    # Si se agotaron los intentos, va a fallidos definitivos
                    fallidos.append({
                        "registro": reg,
                        "error": f"Agotados {max_intentos} intentos. Último error: {str(e)}"
                    })
                    enviado_con_exito = True
                    break
            except Exception as e:
                # Cualquier otro error inesperado no se reintenta
                fallidos.append({
                    "registro": reg,
                    "error": f"Error inesperado: {str(e)}"
                })
                enviado_con_exito = True
                break
                
        if enviado_con_exito:
            continue

    return exitosos, fallidos

def consultar_resultados(url_base, id_equipo):
    """
    Realiza la consulta GET final (Punto 9) para verificar las mediciones 
    registradas en el servidor a nombre de nuestro equipo.
    """
    endpoint = f"{url_base.rstrip('/')}/api/v1/mediciones"
    
    headers = {
        "X-Equipo": id_equipo
    }
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        response.raise_for_status()
        
        return {
            "estado": "EXITO",
            "codigo": response.status_code,
            "datos": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "estado": "ERROR",
            "detalle": f"No se pudo consultar el servidor: {str(e)}"
        }
