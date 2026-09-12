# Contrato API institucional

## 1. Información general

La API institucional permite registrar y consultar mediciones meteorológicas normalizadas.

Cada equipo recibirá:

* una URL base;
* un identificador de equipo.

---

# 2. Registrar una medición

## Endpoint

```text
POST /api/v1/mediciones
```

## Headers requeridos

```text
Content-Type: application/json
X-Equipo: <identificador_equipo>
```

## Body requerido

| Campo         | Tipo   | Obligatorio | Restricción                     |
| ------------- | ------ | ----------: | ------------------------------- |
| ciudad        | string |          Sí | No vacío                        |
| pais          | string |          Sí | No vacío                        |
| latitud       | number |          Sí | -90 a 90                        |
| longitud      | number |          Sí | -180 a 180                      |
| temperatura_c | number |          Sí | Numérico                        |
| humedad       | number |          Sí | 0 a 100                         |
| viento_kmh    | number |          Sí | Mayor o igual a 0               |
| fecha_hora    | string |          Sí | Fecha y hora válida             |
| origen        | string |          Sí | Valor permitido por el contrato |

La API espera los nombres de campo definidos en este contrato.

---

# 3. Respuestas de registro

La operación puede producir los siguientes códigos HTTP:

| Código | Significado            |
| -----: | ---------------------- |
|    201 | Registro aceptado      |
|    400 | Solicitud incorrecta   |
|    409 | Conflicto              |
|    422 | Datos no aceptados     |
|    500 | Error interno          |
|    503 | Servicio no disponible |

La respuesta del servidor será un objeto JSON con información sobre el resultado de la operación.

El cliente debe interpretar el código HTTP y el contenido de la respuesta.

---

# 4. Consultar mediciones

## Endpoint

```text
GET /api/v1/mediciones
```

## Query parameter requerido

```text
equipo
```

## Respuesta exitosa

```text
HTTP 200
```

La respuesta contendrá:

* identificador del equipo;
* número de registros;
* mediciones registradas.

El servidor puede incluir campos adicionales generados durante el almacenamiento.

---

# 5. Reglas generales

La API realiza validación independiente de los datos recibidos.

Una medición validada localmente puede ser rechazada por el servidor.

Las respuestas `4xx` no deben reintentarse automáticamente.

Las respuestas `5xx` pueden considerarse errores transitorios.

El cliente debe manejar adecuadamente errores de comunicación, respuestas inválidas y códigos HTTP no exitosos.

Este documento constituye el contrato oficial de integración.
