import requests

def enviar_mediciones(registros_validos, url_base, id_equipo):
    """
    Envia cada registro valido a la API institucional según el CONTRATO_API.md
    """
    endpoint = f"{url_base.rstrip('/')}/api/v1/mediciones"

    headers = {
        "Content-Type": "application/json",
        "X-Equipo": id_equipo
    }

    exitosos = []
    fallidos = []

    for reg in registros_validos:
        try:
            response = requests.post(endpoint, json=reg, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                exitosos.append(reg)
            else:
                fallidos.append({
                    "registro": reg,
                    "status_code": response.status_code,
                    "respuesta": response.text
                })
        except Exception as e:
            fallidos.append({
                "registro": reg,
                "error": f"Error de conexión: {str(e)}"
            })

    return exitosos, fallidos
