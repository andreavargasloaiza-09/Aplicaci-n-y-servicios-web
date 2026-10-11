# Guía de Trabajo Práctico Experimental — Taller 2

**API para adquisición, validación y consulta de datos IoT con FastAPI, MQTT y PostgreSQL**

**Integrantes:**
Samuel Montoya Galeano  
Andrea Vargas Loaiza

**Asignatura.**  
APLICACIÓN Y SERVICIOS WEB 580202009-1

**Fecha.**  
10 de Octubre del 2026

**Sensor asignado.**  
ENV-002

**Tópico MQTT utilizado.**  
iot/sensors/ENV-002/data

---

| Campo | Valor |
|---|---|
| **Código de guía** | 002 |
| **Laboratorio** | Laboratorio DevOps |
| **Tiempo de trabajo práctico estimado** | 4 días |
| **Asignatura** | Aplicaciones y Servicios Web |
| **Programa académico** | Tecnología en Desarrollo de Software |
| **Elaborado por** | Juan Carlos Morales Guerra |
| **Revisado por** | Juan Carlos Morales Guerra |
| **Versión** | 001 |
| **Fecha** | 07-10-2026 |

---

## 1. Competencias, Contenido Temático e Indicador de Logro

| Competencias | Contenido Temático | Indicador de Logro |
|---|---|---|
| Diseñar e implementar una API para recibir, validar, almacenar y consultar datos provenientes de un sensor IoT, aplicando separación de responsabilidades y persistencia en PostgreSQL. | FastAPI. Pydantic. SQLAlchemy ORM. PostgreSQL. CRUD. Claves primarias y foráneas. Endpoints HTTP. Códigos de respuesta HTTP. MQTT. Validación de payloads. Consultas por identificador, magnitud y rango de fecha. Git y GitHub. | El estudiante integra un consumidor MQTT con una API desarrollada en FastAPI, valida los datos recibidos, consulta la configuración del sensor mediante ORM, almacena las mediciones válidas en PostgreSQL y expone endpoints de consulta con manejo adecuado de errores. |

---

## 2. Fundamento Teórico

Una **API REST** permite que aplicaciones diferentes intercambien información mediante solicitudes HTTP. En este taller, FastAPI se utilizará para exponer endpoints que permitan consultar sensores, magnitudes y mediciones almacenadas.

**FastAPI** es un framework de Python orientado al desarrollo de APIs. Permite definir rutas, parámetros, respuestas HTTP y modelos de validación. También genera documentación automática mediante OpenAPI.

**Pydantic** permite definir la estructura esperada de los datos y validar campos obligatorios, tipos de datos y formatos. En esta práctica se utilizará para validar el contenido de los mensajes recibidos y los datos utilizados por la API.

**SQLAlchemy ORM** permite representar tablas de PostgreSQL mediante clases de Python. El ORM se utilizará para consultar los sensores y sus magnitudes, trabajar con claves primarias y foráneas y almacenar las mediciones válidas.

**CRUD** corresponde a las operaciones Create, Read, Update y Delete. La existencia de una capa `crud/` no implica que todas las entidades deban implementar las cuatro operaciones. Cada módulo deberá implementar únicamente las operaciones autorizadas para esa entidad.

### MQTT

**MQTT (Message Queuing Telemetry Transport)** es un protocolo de mensajería ligero utilizado frecuentemente en sistemas IoT. Su funcionamiento se basa en un modelo de publicación y suscripción.

Los elementos principales son:

- **Publicador:** dispositivo o aplicación que envía mensajes.
- **Broker:** servicio que recibe los mensajes y los distribuye.
- **Suscriptor:** aplicación que recibe los mensajes de uno o varios tópicos.
- **Tópico:** ruta utilizada para organizar los mensajes.

En esta práctica, el sensor publica mediciones en un tópico MQTT y la aplicación desarrollada por el estudiante actúa como suscriptor.

```mermaid
flowchart LR
    A[Sensor] -->|Publica medición| B[Broker MQTT]
    B -->|Entrega mensaje| C[Aplicación del estudiante]
    C --> D[Pydantic]
    D --> E[SQLAlchemy ORM]
    E --> F[(PostgreSQL)]
    G[Cliente HTTP] --> H[FastAPI]
    H --> E
```

---

## 3. Objetivos

### Objetivo General

Desarrollar una aplicación backend que reciba datos IoT mediante MQTT, valide la información con Pydantic, consulte la configuración del sensor mediante SQLAlchemy ORM, almacene las mediciones válidas en PostgreSQL y permita consultarlas mediante endpoints desarrollados con FastAPI.

### Objetivos Específicos

- Consumir datos desde un tópico MQTT asignado.
- Interpretar el modelo de datos suministrado.
- Implementar modelos SQLAlchemy ORM.
- Implementar esquemas Pydantic.
- Validar estructura, tipos de datos y timestamp.
- Validar sensor, magnitud, unidad y rango mediante ORM y lógica de negocio.
- Almacenar mediciones válidas en PostgreSQL.
- Implementar consultas por ID, magnitud, histórico y rango de fechas.
- Manejar respuestas y errores HTTP.
- Organizar el código mediante separación de responsabilidades.
- Documentar y evidenciar el funcionamiento en GitHub.

---

## 4. Recursos Requeridos

### Equipos

- Computador personal o estación de trabajo por estudiante.

### Herramientas de Software

- Python 3.10 o superior.
- FastAPI.
- PostgreSQL.
- SQLAlchemy.
- Pydantic.
- Uvicorn.
- Cliente MQTT para Python.
- Git.
- Cuenta en GitHub.
- Editor de código.

### Infraestructura suministrada

**Broker MQTT**

```text
emqx.coriotlab.co
```

La estructura general de los tópicos será:

```text
iot/sensors/{sensor_id}/data
```

Ejemplo:

```text
iot/sensors/TEST-001/data
```

El tópico real será suministrado por el docente.

**Base de datos PostgreSQL**

El host, las credenciales y el nombre de la base serán suministrados por el docente.

### Recursos disponibles en el repositorio

El repositorio del taller contiene:

- `data-model.md`: descripción de tablas, campos, tipos de datos, claves y relaciones.
- `mqtt_example.py` : ejemplo para conectarse al broker, suscribirse a un tópico y visualizar mensajes MQTT.

El script de ejemplo es una guía de consumo MQTT se debe cambiar el topico por el asignado para cada grupo.

### Asignación de sensores

Cada grupo recibirá un sensor asignado por el docente.

La asignación podrá realizarse hasta:

**viernes 9 de octubre de 2026**

Después de esta fecha no se asignarán sensores.

El identificador entregado corresponde al campo `codigo` de la tabla `sensores`.

---

## 5. Aspectos de Seguridad

La práctica corresponde a una actividad de desarrollo de software y no implica riesgos físicos o químicos asociados al uso de equipos experimentales.

Se deben tener en cuenta las siguientes consideraciones:

- No incluir credenciales reales en el código fuente.
- No subir archivos `.env` al repositorio.
- Utilizar variables de entorno para credenciales y parámetros de conexión.
- Mantener `.env` dentro del `.gitignore`.
- Realizar copias de seguridad mediante commits frecuentes.
- No modificar datos de otros grupos.
- Utilizar únicamente el sensor y tópico asignados.

---

## 6. Procedimiento o Metodología para el Desarrollo

La práctica se desarrollará en equipos de trabajo de maximo dos personas, no se permiten equipos de tres si excepción.

### Actividad 1: Configuración Inicial del Proyecto

1. Crear el branch taller-2 en el repositorio en GitHub del curso.
2. Crear y activar un entorno virtual.
3. Instalar las dependencias.
4. Crear `requirements.txt`.
5. Crear `.gitignore`.
6. Configurar las variables de entorno necesarias.
7. Verificar la conexión con PostgreSQL.
8. Ejecutar el script MQTT de ejemplo y comprobar la recepción de mensajes del sensor asignado.

---

### Actividad 2: Comprensión del Problema y del Modelo de Datos

#### A. Planteamiento del Problema

Una infraestructura IoT dispone de sensores destinados al monitoreo de variables relacionadas con calidad del aire, calidad del agua, gases y condiciones ambientales.

Cada sensor puede medir una o varias magnitudes y publica periódicamente sus datos mediante el protocolo UDP MQTT.

La aplicación desarrollada debe:

1. conectarse al broker MQTT;
2. suscribirse al tópico del sensor asignado;
3. recibir y decodificar los mensajes;
4. validar la estructura y los tipos de datos;
5. consultar la configuración almacenada en PostgreSQL;
6. validar sensor, magnitud, unidad y rango;
7. almacenar únicamente mensajes válidos;
8. exponer endpoints de consulta mediante FastAPI.

#### B. Payload

Los sensores publican mensajes JSON.

Ejemplo:

```json
{
  "sensor_id": "TEST-001",
  "timestamp": "2026-10-07T16:25:30Z",
  "measurements": {
    "temperature": {
      "value": 24.6,
      "unit": "C"
    }
  }
}
```

El campo `sensor_id` recibido mediante MQTT corresponde al campo `codigo` de la tabla `sensores`; no corresponde a la clave primaria numérica `id` en la base de datos.

Cada grupo deberá revisar el payload real recibido y documentar:

- magnitudes;
- unidades;
- tipos de datos;
- estructura;
- timestamp.

#### C. Modelo de Datos

El modelo de datos se encuentra en:

```text
data-model.md
```

Los estudiantes deberán interpretarlo y construir los modelos ORM correspondientes.

El catálogo de sensores y magnitudes ya existe en la base de datos y es suministrado por el docente.

La aplicación puede consultar este catálogo, pero no crear, modificar ni eliminar sensores o magnitudes.

---

### Actividad 3: Implementación de Modelos, Schemas y CRUD

La solución deberá separar responsabilidades.

Estructura mínima:

```text
app/
├── main.py
├── schemas/
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── models/
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── crud/
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── api/
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── mqtt/
│   └── client.py
└── database/
    └── connection.py
```

Cada tabla debe tener su archivo correspondiente en:

- `schemas/`
- `models/`
- `crud/`
- `api/`

#### Validaciones con Pydantic

Pydantic deberá verificar:

- estructura del mensaje;
- campos obligatorios;
- tipos de datos;
- formato del timestamp.

#### Validaciones con ORM y lógica de negocio

Después de la validación de estructura, la aplicación deberá verificar:

- existencia del sensor;
- estado del sensor;
- relación entre sensor y magnitud;
- correspondencia de la unidad;
- consistencia de las claves foráneas.

Si un payload contiene varias magnitudes, **solo se almacenará si todas son válidas**.

Cada magnitud contenida en un payload válido debe almacenarse como un registro independiente en la tabla `mediciones`.

Todas las mediciones generadas a partir del mismo payload deben conservar el mismo `timestamp_utc`.

---

### Actividad 4: Integración MQTT y Almacenamiento

La aplicación deberá consumir los mensajes del tópico asignado.

El servicio MQTT puede publicar mensajes válidos e inválidos de forma intencional. La aplicación debe procesar ambos casos y almacenar únicamente los mensajes que superen todas las validaciones.

El timestamp recibido desde MQTT se encuentra en UTC.

La aplicación deberá:

1. validar el timestamp;
2. almacenarlo conservando la referencia UTC;
3. convertirlo en las respuestas GET a hora local de Colombia;
4. presentar la fecha y hora en un formato legible y consistente.

Cada grupo deberá recolectar datos del sensor asignado durante al menos:

```text
20 minutos
```

---

### Actividad 5: Desarrollo de Endpoints

La API debe ofrecer como mínimo operaciones equivalentes a:

```text
GET /sensores
GET /sensores/{id}
GET /sensores/por-codigo/{codigo}

GET /sensores/{id}/magnitudes
GET /sensor-magnitudes/{id}

GET /mediciones/{id}
GET /sensores/{id}/mediciones
GET /sensores/{id}/ultima-medicion
```

La consulta histórica debe permitir combinar filtros.

Ejemplos:

```text
GET /sensores/{id}/mediciones?desde=...&hasta=...

GET /sensores/{id}/mediciones?magnitud=temperature

GET /sensores/{id}/mediciones?limit=10

GET /sensores/{id}/mediciones?magnitud=temperature&desde=...&hasta=...&limit=10
```

El parámetro `limit` permite consultar las últimas N mediciones.

---

### Actividad 6: Pruebas y Evidencias

Los códigos HTTP se evaluarán únicamente en las solicitudes realizadas a los endpoints FastAPI.

Los errores detectados durante el procesamiento MQTT se deberán manejar internamente y evidenciar mediante registros de ejecución y comprobación de que los datos inválidos no fueron almacenados.

Se deberán demostrar los siguientes códigos HTTP:

```text
200
400
404
422
```

#### Evidencias obligatorias

| # | Prueba | Evidencia esperada |
|---|---|---|
| 1 | Recepción MQTT | Mensaje recibido desde el tópico asignado |
| 2 | Medición válida | Registro almacenado en PostgreSQL |
| 3 | Sensor inexistente | Mensaje rechazado | 
| 4 | Unidad incorrecta | Mensaje rechazado | 
| 5 | Tipo de dato incorrecto | Mensaje rechazado |
| 6 | Magnitud incorrecta | Mensaje rechazado | 
| 7 | Timestamp inválido | Mensaje rechazado | 
| 8 | Consulta por ID existente | Respuesta correcta | 
| 9 | Consulta por ID inexistente | `404` | 
| 10 | Consulta histórica | Datos históricos retornados | 
| 11 | Consulta por rango de fechas | Datos filtrados | 
| 12 | Rango `desde > hasta` | `400` | 
| 13 | Validación HTTP incorrecta | `422` | 
| 14 | Última medición | Registro más reciente | 
| 15 | Últimas N mediciones | Uso correcto de `limit` | 
| 16 | Filtro por magnitud | Resultado filtrado | 
| 17 | Claves foráneas | Relación implementada correctamente | 
| 18 | Separación de responsabilidades | Organización correcta del código | 

Para cada prueba se deberá indicar:

- datos de entrada;
- resultado obtenido;
- código HTTP cuando aplique;
- registro almacenado o rechazado;
- archivo y función donde se implementa la lógica relacionada;
- breve explicación.

No es necesario incluir capturas del código fuente.

| # | Datos de entrada | Resultado obtenido | Código HTTP | Registro almacenado / rechazado | Archivo y función de la lógica | Breve explicación | Captura / Imagen |
|---|---|---|---|---|---|---|---|
| **1** | Inicio del servidor FastAPI y ejecución del evento `@app.on_event("startup")` | Log en consola: `Iniciando cliente MQTT...` y `Application startup complete.` | N/A | N/A | `app/main.py` (`startup_event`) y `app/mqtt/client.py` (`conectar_mqtt`) | Al arrancar la aplicación Web/API, se inicializa automáticamente el cliente MQTT y se establece la conexión con el broker en segundo plano.| ![Evidencia 1](evidencias/evd_01.png) |
| **2** | Tópico: `iot/sensors/ENV-002/data`<br>Payload JSON con lecturas del simulador | Log en consola: `Éxito: Se guardaron 3 mediciones del sensor ENV-002.` | N/A | **Almacenado** | `app/mqtt/client.py` (`on_message`), `app/crud/crud_medicion.py` (`guardar_mediciones`) | El cliente MQTT procesa los mensajes entrantes, valida la estructura del payload y almacena las lecturas en la base de datos.| ![Evidencia 2](evidencias/evd_02.png) |
| **3** | `GET /sensores/{id}/mediciones`<br>Params: `id = 999`, `limit = 100` | Respuesta JSON: `{"detail": "Sensor no encontrado"}` | `404 Not Found` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Se valida la existencia del sensor en la BD antes de consultar el historial. Al no existir el ID 999, el sistema retorna una excepción HTTP 404. | ![Evidencia 3](evidencias/evd_03.png) |
| **4** | Tópico: `iot/sensors/ENV-002/data`<br>Payload con unidad inválida para `humidity` | Log en consola: `Rechazado: Unidad incorrecta para humidity. Esperada %` | N/A | **Rechazado** | `app/mqtt/client.py` (`procesar_mensaje`) | En el paso 3 de la función se valida que `magnitud_db.unidad == mag_data.unit`. Al detectar una unidad diferente a `%`, detiene la ejecución con un `return`.| ![Evidencia 4](evidencias/evd_4.png) |
| **5** | Tópico: `iot/sensors/ENV-002/data`<br>Payload JSON con propiedad incompleta (falta `value` en `illuminance`) | Log en consola: `Rechazado: Error de validación Pydantic: 1 validation error for MQTTPayload measurements.illuminance.value Field required` | N/A | **Rechazado** | `app/mqtt/client.py` (`procesar_mensaje`) | En el paso 1, Pydantic detecta que falta la clave `value` obligatoria en `illuminance`, elevando una `ValidationError` que aborta el guardado. | ![Evidencia 5](evidencias/evd_05.png) |
| **6** | Tópico: `iot/sensors/ENV-002/data`<br>Payload con magnitud incorrecta / no asociada (`co2`) | Log en consola: `Rechazado: Magnitud co2 no asociada al sensor.` | N/A | **Rechazado** | `app/mqtt/client.py` (`procesar_mensaje`) | Valida contra la base de datos que la magnitud pertenezca al sensor. Al recibir `co2` no vinculada, la función `get_sensor_magnitud_by_sensor_and_nombre` retorna `None` y rechaza el mensaje. | ![Evidencia 6](evidencias/evd_06.png) |
| **7** |Tópico: `iot/sensors/ENV-002/data`<br>Payload con `timestamp` inválido (`"not-a-timestamp"`) | Log en consola: `Rechazado: Error de validación Pydantic: 1 validation error for MQTTPayload timestamp... Input should be a valid datetime or date` | N/A | **Rechazado** | `app/mqtt/client.py` (`procesar_mensaje`) | En el paso 1, Pydantic valida que el campo `timestamp` cumpla con el formato ISO `datetime`. Al recibir una cadena no válida, eleva una `ValidationError` y detiene el proceso. | ![Evidencia 7](evidencias/evd_07.png) |
| **8** | `GET /sensores/{id}`<br>Params: `id = 1` | Objeto JSON con el detalle del sensor ID 1 (`AQ-001`). | `200 OK` | N/A (Consulta) | `app/api/sensor.py` (`obtener_sensor`) | Consulta la tabla de sensores por la clave primaria ID 1. Al existir en la BD, retorna el objeto del sensor parametrizado. | ![Evidencia 8](evidencias/evd_08.png) |
| **9** | `GET /sensores/{id}`<br>Params: `id = 16` | Respuesta JSON: `{"detail": "Sensor no encontrado"}` | `404 Not Found` | N/A (Consulta) | `app/api/sensor.py` (`obtener_sensor`) | Se consulta un sensor inexistente (ID 16). La función valida contra la base de datos y, al no hallar el registro, retorna una excepción HTTP 404. | ![Evidencia 9](evidencias/evd_09.png) |
| **10** | `GET /sensores/{id}/mediciones`<br>Params: `id = 2`, `limit = 100` | Listado JSON de mediciones históricas con marca de tiempo convertida a `timestamp_local`. | `200 OK` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Valida la existencia del sensor ID 2 en la BD, recupera su historial de mediciones, aplica la conversión de fecha a hora local y retorna la lista con código HTTP 200. | ![Evidencia 10](evidencias/evd_10.png) |
| **11** | `GET /sensores/2/mediciones`<br>Params: `desde = 2026-10-08T00:00:00`, `hasta = 2026-10-08T23:59:59` | Arreglo JSON filtrado con mediciones dentro del rango temporal especificado. | `200 OK` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Valida el rango de fechas e incluye las condiciones `>= desde` y `<= hasta` en la consulta ORM a la BD, retornando los registros correspondientes. | ![Evidencia 11](evidencias/evd_11.png) |
| **12** | `GET /sensores/2/mediciones`<br>Params: `desde = 2026-10-10T10:00:00`, `hasta = 2026-10-10T08:00:00` | Respuesta JSON: `{"detail": "La fecha 'desde' no puede ser mayor a 'hasta'"}` | `400 Bad Request` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Evalúa si `desde > hasta`. Al ser incoherente el rango temporal, detiene la ejecución y retorna una excepción HTTP 400. | ![Evidencia 12](evidencias/evd_12.png) |
| **13** | `GET /sensores/2/mediciones`<br>Params: `hasta = "fecha_invalida"` | Respuesta JSON de validación: `Input should be a valid datetime or date, invalid character in year` | `422 Unprocessable Content` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | FastAPI convalida los tipos de datos declarados. Al enviar una cadena no convertible a fecha en el query param `hasta`, Pydantic intercepta la petición y retorna un error 422. | ![Evidencia 13](evidencias/evd_13.png) |
| **14** | `GET /sensores/2/ultima-medicion`<br>Param: `id = 2` | Objeto JSON con la última lectura registrada (`id: 10381`, timestamp de las 21:57:43). | `200 OK` | N/A (Consulta) | `app/api/medicion.py` (`obtener_ultima_medicion`) | Realiza una consulta con ordenamiento descendente por marca de tiempo (`DESC`) y `LIMIT 1`, devolviendo la medición con el timestamp más reciente registrado para el sensor. | ![Evidencia 14](evidencias/evd_14.png) |
| **15** | `GET /sensores/2/mediciones`<br>Params: `id = 2`, `limit = 1` | Arreglo JSON con exactamente 1 registro (la medición más reciente). | `200 OK` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Utiliza el parámetro de consulta `limit` para truncar la respuesta de la BD a un único registro ($N=1$) mediante la cláusula `.limit()`. | ![Evidencia 15](evidencias/evd_15.png) |
| **16** | `GET /sensores/2/mediciones`<br>Params: `id = 2`, `magnitud = "pm2_5"` | Arreglo JSON de mediciones filtrado exclusivamente por la magnitud solicitada (`pm2_5`). | `200 OK` | N/A (Consulta) | `app/api/medicion.py` (`obtener_mediciones_historicas`) | Realiza un JOIN entre `Medicion` y `SensorMagnitud` para aplicar el filtro por el nombre de la magnitud especificada en la petición. | ![Evidencia 16](evidencias/evd_16.png) |
| **17** | `GET /sensores/2/mediciones`<br>Params: `id = 2`, `magnitud = "pm2_5"` | Respuesta JSON donde se valida la resolución correcta de la clave foránea entre `mediciones` y `sensores_magnitudes`. | `200 OK` | N/A (Relación relacional) | `app/crud/medicion.py` | La consulta valida e integra las llaves foráneas en la base de datos. La respuesta confirma que la relación relacional está correctamente vinculada e implementada. | ![Evidencia 17](evidencias/evd_16.png) |
| **18** | Árbol de archivos del proyecto (`app/`) | Módulos organizados por capas (`api`, `crud`, `models`, `schemas`). | `N/A` | N/A (Arquitectura) | Estructura modular del proyecto | Demuestra la separación de responsabilidades organizando el código en carpetas independientes para peticiones HTTP, operaciones en BD, modelos relacionales y esquemas de validación. | ![Evidencia 18](evidencias/evd_18.png) |

---

### Actividad 7: Trabajo Colaborativo

El equipo deberá evidenciar el trabajo colaborativo mediante Git y GitHub.

Requisitos mínimos:

- Cada integrante debe tener commits identificables.
- Los mensajes de commit deben ser descriptivos.
- El historial debe evidenciar participación del equipo.
- El README debe indicar el aporte de cada integrante.

---

## 7. Resultado Esperado del Taller

Al finalizar el taller, cada equipo deberá disponer de una aplicación funcional que:

- consuma datos desde MQTT;
- valide mensajes mediante Pydantic;
- consulte sensores y magnitudes mediante ORM;
- valide unidades y rangos;
- almacene únicamente mediciones válidas;
- conserve las relaciones mediante claves foráneas;
- exponga endpoints con FastAPI;
- permita consultas históricas;
- permita filtrar por magnitud y fechas;
- permita consultar la última medición y las últimas N;
- convierta el timestamp UTC a hora local de Colombia en los GET;
- maneje correctamente errores HTTP;
- mantenga una estructura modular del código.

Toda la solución y sus evidencias deberán quedar disponibles en el repositorio GitHub del equipo.

---

## 8. Parámetros para Elaboración del Informe

El informe del taller deberá presentarse en formato **README.md** dentro del repositorio del proyecto.

No se aceptarán informes externos en Word o PDF.

### Contenido del README.md

#### 1. Información General

- Nombre del proyecto.
- Integrantes.
- Asignatura.
- Fecha.
- Sensor asignado.
- Tópico MQTT utilizado.

### 2. Descripción del Sistema

#### Problema Resuelto
El sistema resuelve la necesidad de monitorear, centralizar y consultar en tiempo real las mediciones ambientales recolectadas por estaciones IoT. Permite procesar el flujo constante de datos a través de MQTT, validar las mediciones frente a reglas de rango y unidades, almacenar el historial de lecturas de forma estructurada, garantizar la integridad referencial y ofrecer una API REST para consultar la información de manera filtrada, paginada y ajustada a la zona horaria local.

#### Arquitectura Implementada
El backend está desarrollado bajo una arquitectura limpia y desacoplada en capas utilizando **FastAPI** y **SQLAlchemy ORM**:
* **Capa de API (`app/api`):** Define los endpoints REST, gestiona el enrutamiento HTTP y las respuestas.
* **Capa de Esquemas (`app/schemas`):** Utiliza Pydantic para la validación estricta de tipos de entrada, payloads MQTT y serialización de salida.
* **Capa CRUD (`app/crud`):** Encapsula la lógica de negocio y las operaciones de consulta/escritura a la base de datos.
* **Capa de Modelos (`app/models`):** Define la estructura relacional de las tablas y sus llaves foráneas (`sensores`, `sensores_magnitudes`, `mediciones`).
* **Capa de Base de Datos (`app/database`):** Gestiona la conexión y las sesiones con la base de datos mediante SQLAlchemy.
* **Cliente MQTT (`app/mqtt`):** Suscriptor encargado de recibir y procesar en tiempo real las lecturas enviadas por los dispositivos IoT en segundo plano.

#### Magnitudes y Unidades Recibidas
El sistema procesa y valida dinámicamente las siguientes magnitudes físicas según la configuración del sensor:
* **`co2` / `eco2`**: Dióxido de carbono y dióxido de carbono equivalente (Unidad: `ppm`).
* **`tvoc`**: Compuestos Orgánicos Volátiles Totales (Unidad: `ppb`).
* **`ch4`**: Metano (Unidad: `ppm`).
* **`humidity`**: Humedad relativa (Unidad: `%`).
* **`temperature`**: Temperatura ambiental (Unidad: `C`).
* **`pm10` / `pm2_5` / `pm1_0`**: Material particulado (Unidad: `ug/m3`).

#### Payload Real del Sensor
Estructura JSON recibida a través del broker MQTT y procesada por la función `procesar_mensaje` mediante el esquema `MQTTPayload`:

```json
{
  "sensor_id": "ENV-002",
  "timestamp": "2026-10-08T21:57:43Z",
  "measurements": {
    "temperature": {
      "value": 24.5,
      "unit": "C"
    },
    "humidity": {
      "value": 60.0,
      "unit": "%"
    },
    "co2": {
      "value": 450.0,
      "unit": "ppm"
    },
    "tvoc": {
      "value": 120.0,
      "unit": "ppb"
    }
  }
}
```

#### 3. Configuración del Entorno

- Creación del entorno virtual.
- Instalación de dependencias.
- Uso de `requirements.txt`.
- Variables de entorno requeridas, sin valores sensibles.

#### 4. Base de Datos

- Descripción de la conexión.
- Tablas utilizadas.
- Relaciones implementadas.
- Correspondencia con `data-model.md`.

#### 5. Organización del Código

Describir la función de:

- `schemas/`
- `models/`
- `crud/`
- `api/`
- `mqtt/`
- `database/`

#### 6. Endpoints Implementados

Tabla con:

#### 6. Endpoints Implementados

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/sensores` | Lista todos los sensores registrados en el sistema. |
| `GET` | `/sensores/{id}` | Obtiene la información detallada de un sensor específico según su ID. |
| `GET` | `/sensores/por-codigo/{codigo}` | Busca y retorna la información de un sensor utilizando su código único. |
| `GET` | `/sensores/{id}/magnitudes` | Lista todas las magnitudes o variables físicas asociadas a un sensor determinado. |
| `GET` | `/sensor-magnitudes/{id}` | Obtiene los detalles de una relación específica entre un sensor y una magnitud por su ID. |
| `GET` | `/sensores/{id}/mediciones` | Consulta el historial de mediciones de un sensor. Permite filtrado por rango de fechas (`desde`, `hasta`), magnitud (`magnitud`) y límite de registros (`limit`). |
| `GET` | `/mediciones/{id}` | Obtiene los detalles de una lectura de medición individual por su ID. |
| `GET` | `/sensores/{id}/ultima-medicion` | Devuelve la última lectura registrada (la más reciente en el tiempo) para un sensor específico, convirtiendo la marca de tiempo a la hora local. |

#### 7. Evidencias de Funcionamiento

Crear dentro del repositorio una carpeta:

```text
evidencias/
```

Las evidencias deberán cubrir las pruebas obligatorias de la Actividad 6.

Para cada evidencia se debe indicar el archivo y la función relacionados con la implementación.

#### 8. Control de Versiones

- Enlace al repositorio.
- Evidencia de commits.
- Aporte de cada integrante.

#### 9. Conclusiones

- **Principales aprendizajes:**
  - Implementación de una arquitectura limpia por capas en FastAPI (API, CRUD, Modelos, Esquemas), logrando un código desacoplado, mantenible y escalable.
  - Integración efectiva de clientes MQTT en segundo plano para la ingesta en tiempo real de datos IoT, validando esquemas dinámicos mediante Pydantic antes de su persistencia.
  - Gestión rigurosa de integridad referencial y mapeo relacional de base de datos (`ForeignKey` y `relationship` en SQLAlchemy) para asociar sensores, magnitudes y mediciones.

- **Dificultades encontradas:**
  - Descalce en la serialización de respuestas HTTP (`ResponseValidationError`) por la ausencia del atributo `timestamp_local` al retornar objetos ORM directos de la base de datos.
  - Complejidad en la sincronización de marcas de tiempo UTC almacenadas en la base de datos frente a la presentación de hora local requerida por el cliente.
  - Discrepancias en el ordenamiento temporal al consultar la "última medición", donde la ausencia de un ordenamiento descendente explícito retornaba el registro más antiguo en lugar del más reciente.

- **Soluciones aplicadas:**
  - Adaptación en la capa API para calcular y convertir explícitamente el `timestamp_utc` a la zona horaria local (`astimezone()`) antes de serializar la respuesta en el modelo `MedicionResponse`.
  - Configuración de consultas ORM con cláusulas `ORDER BY timestamp_utc DESC` y `LIMIT 1` para garantizar la recuperación precisa del registro temporal más reciente.
  - Implementación de validaciones estrictas en la ingesta MQTT que verifican la existencia del sensor, el rango de valores permitido (`valor_minimo` y `valor_maximo`) y la concordancia de unidades antes de guardar en base de datos.

### Requisitos del Repositorio

El repositorio debe:

- contener el código fuente completo;
- incluir `README.md`;
- incluir `requirements.txt`;
- incluir `.gitignore`;
- incluir `data-model.md`;
- contener las evidencias;
- no incluir `.env` con credenciales reales.

---

## 9. Disposición de Residuos

La actividad descrita en esta guía no genera residuos físicos o químicos. En consecuencia, no se requiere un procedimiento específico de disposición de residuos.

---

## 10. Bibliografía

- FastAPI. *FastAPI Documentation*. https://fastapi.tiangolo.com
- Pydantic. *Pydantic Documentation*. https://docs.pydantic.dev
- SQLAlchemy. *SQLAlchemy Documentation*. https://docs.sqlalchemy.org
- PostgreSQL Global Development Group. *PostgreSQL Documentation*. https://www.postgresql.org/docs/
- OASIS. *MQTT Version 5.0*. https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
- Python Software Foundation. *Python Documentation*. https://docs.python.org
- Chacon, S., & Straub, B. (2014). *Pro Git*. Apress.
