# Taller 1 — Integración de datos entre aplicaciones

## Propósito

Construir en Python un cliente integrador capaz de leer datos provenientes de distintas fuentes, adaptarlos a un contrato institucional, validarlos y comunicarse con una API mediante HTTP.

La API será suministrada y desplegada por el docente. El objetivo del taller no es desarrollar la API, sino construir correctamente el cliente que se integra con ella.

## Escenario

Una universidad recibe información meteorológica proveniente de diferentes proveedores. Cada proveedor representa los datos de forma distinta y puede contener registros incompletos o inválidos.

El equipo debe desarrollar una aplicación que:

1. lea los datasets suministrados;
2. analice las diferencias entre sus estructuras;
3. transforme cada registro al contrato institucional;
4. valide localmente los datos;
5. registre mediante HTTP las mediciones válidas;
6. interprete las respuestas del servidor;
7. consulte posteriormente qué registros fueron almacenados;
8. genere evidencias del proceso de integración.

## Material suministrado

```text
taller_1/
├── datos/
│   ├── proveedor_a.json
│   └── proveedor_b.csv
├── CONTRATO_API.md
├── requirements.txt
└── README.md
```

Además, cada equipo recibirá:

- URL base de la API.
- Identificador de equipo.

No se suministrará Swagger ni OpenAPI.

`CONTRATO_API.md` constituye la documentación oficial de integración.

## 1. Análisis de los contratos

Antes de programar, compare:

- Proveedor A.
- Proveedor B.
- Contrato institucional.

Construya una tabla que permita identificar correspondencias entre los campos de los proveedores y el contrato institucional, considerando cuando corresponda:

- nombre;
- tipo;
- unidad;
- formato;
- transformación necesaria.

No se suministra una lista explícita de transformaciones.

| Campo Contrato API | Tipo API | Fuente Proveedor A | Transformación Proveedor A | Fuente Proveedor B | Transformación Proveedor B |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ciudad** | string | station.city_name | Extraer texto de objeto anidado | Columna 2 | Extraer texto (posición 2) |
| **pais** | string | station.country_code | Extraer texto de objeto anidado | Columna 3 | Extraer texto (posición 3) |
| **latitud** | number | location.lat | Convertir a float | Columna 4 | Convertir a float |
| **longitud** | number | location.lon | Convertir a float | Columna 5 | Convertir a float |
| **temperatura_c** | number | measurements.temperature_f | Convertir de °F a °C: (temp_f - 32) * 5 / 9 | Columna 6 | Convertir a float (ya viene en °C) |
| **humedad** | number | measurements.relative_humidity | Convertir a float | Columna 7 | Convertir a float |
| **viento_kmh** | number | measurements.wind_speed_ms | Convertir de m/s a km/h: wind_ms * 3.6 | Columna 8 | Convertir a float (ya viene en km/h) |
| **fecha_hora** | string | observed_at | Ninguna (ya viene en ISO 8601) | Columna 9 | Parsear DD/MM/YYYY HH:mm a ISO 8601 |
| **origen** | string | source | Extraer string ("weather_provider_a") | Columna 10 | Extraer string ("PB") |

## 2. Lectura de datos

El programa debe procesar todos los registros presentes en:

```text
datos/proveedor_a.json
datos/proveedor_b.csv
```

Los archivos originales no pueden ser modificados.

Para este taller, `procesados` corresponde a la cantidad total de registros identificados en ambos datasets.

## 3. Normalización

Cada registro debe transformarse a una representación compatible con el contrato institucional.

Durante este proceso deben resolverse las diferencias de estructura, tipos, unidades y formato que existan entre las fuentes.

Los valores institucionales permitidos para `origen` son:

```text
proveedor_a
proveedor_b
```

La fecha normalizada debe expresarse en formato ISO 8601.

Si un registro contiene un dato que no puede convertirse al tipo o representación exigida por el contrato institucional, se considera un **error de normalización**.

Los registros con error de normalización:

- no deben enviarse a la API;
- no deben incluirse en `salida/normalizadas.json`;
- deben quedar identificados en el reporte final.

Un registro correctamente normalizado puede todavía ser inválido según las reglas de negocio.

## 4. Validación local

Todo registro normalizado debe ser validado antes de enviarse.

Un registro que puede representarse correctamente con el contrato institucional, pero incumple una regla del contrato, se clasifica como `rechazado_localmente`.

Estos registros:

- sí deben permanecer en `salida/normalizadas.json`;
- no deben enviarse a la API;
- deben quedar identificados en el reporte.

La validación local no reemplaza la validación realizada por el servidor.

## 5. Trazabilidad

Cada registro debe conservar un identificador interno de trazabilidad.

Puede utilizarse el identificador original del proveedor o uno propio derivado de la fuente y la posición del registro.

Este identificador se usa únicamente para evidencias y reporte. No debe enviarse en el body de la API si no pertenece al contrato institucional.

## 6. Evidencia de normalización

El programa debe generar:

```text
salida/normalizadas.json
```

Debe contener todos los registros que pudieron ser convertidos al contrato institucional, incluidos aquellos que posteriormente sean rechazados por la validación local.

## 7. Integración HTTP

Las mediciones que superen la validación local deben enviarse a la API institucional.

Los métodos, rutas, headers, parámetros y estructura de los datos están definidos en `CONTRATO_API.md`.

## 8. Manejo de respuestas y reintentos

El cliente debe interpretar el código HTTP y el contenido de la respuesta.

Debe manejar como mínimo:

```text
201
400
409
422
5xx
```

Las respuestas `4xx` no deben reintentarse automáticamente.

Ante errores `5xx`, timeout o pérdida de conexión, se permite:

- 1 intento inicial;
- hasta 2 reintentos adicionales;
- máximo 3 intentos por registro.

Después de agotar los intentos, el registro debe quedar identificado como error de comunicación.

El programa no debe finalizar abruptamente ante una respuesta HTTP inesperada.

## 9. Consulta de resultados

Al finalizar los envíos, el cliente debe utilizar la operación de consulta definida en `CONTRATO_API.md` para verificar qué mediciones asociadas al equipo fueron registradas.

## 10. Reporte final

El programa debe generar:

```text
salida/reporte.json
```

El reporte debe permitir conocer, como mínimo:

- registros procesados;
- registros normalizados;
- errores de normalización;
- registros válidos localmente;
- registros rechazados localmente;
- registros enviados;
- registros aceptados por la API;
- registros rechazados por la API;
- errores de comunicación.

También debe conservar suficiente trazabilidad para identificar cada registro y su resultado.

## 11. Organización del código

El código debe estar organizado en funciones o módulos con responsabilidades claras.

No se exige una arquitectura específica.

Se evaluará negativamente un único bloque extenso de código sin separación de responsabilidades.

## 12. Manejo de errores

El programa debe manejar de forma controlada situaciones como:

- archivo inexistente;
- JSON no interpretable;
- fila CSV defectuosa;
- pérdida de conexión;
- timeout;
- respuestas HTTP no exitosas;
- respuestas no JSON.

No debe mostrarse un traceback no controlado durante la ejecución normal.

## 13. Configuración y ejecución

La URL de la API y el identificador del equipo deben definirse como constantes configurables al inicio de `integrador.py`:

```text
URL_BASE
EQUIPO
```

Comando principal:

```bash
python integrador.py
```

Las pruebas deberán poder ejecutarse mediante:

```bash
pytest
```

## 14. Pruebas automatizadas

El proyecto debe incluir al menos 5 pruebas automatizadas independientes de la API real.

Deben cubrir como mínimo:

1. una transformación correcta;
2. una conversión de unidades;
3. un registro válido;
4. un registro inválido;
5. un caso límite seleccionado por el equipo.

No se exige una técnica específica para aislar la API.

## 15. Análisis final

Incluya un archivo:

```text
ANALISIS.md
```

Extensión máxima aproximada: dos páginas, sin contar tablas o fragmentos de evidencia.

Debe responder:

1. ¿Qué diferencias encontró entre los contratos de los proveedores?
2. ¿Qué transformaciones fueron necesarias?
3. ¿Qué tipos de errores encontró antes de enviar información?
4. ¿Qué diferencias encontró entre validación local y validación del servidor?
5. ¿Qué decisión de implementación considera más importante y por qué?

Además, incluya evidencia resumida de una ejecución real del programa.

La evidencia debe mostrar, como mínimo:

- cantidad total de registros procesados;
- cantidad normalizada;
- cantidad rechazada localmente;
- cantidad enviada a la API;
- cantidad aceptada y rechazada por la API;
- al menos un caso de error de normalización o validación;
- al menos una respuesta recibida desde la API;
- resultado de la consulta final mediante `GET`.

La evidencia puede presentarse como tabla, fragmentos relevantes de la salida del programa o información tomada de los archivos generados en `salida/`.

No es necesario incluir capturas de pantalla ni copiar la salida completa de ejecución.

## Entregables

```text
proyecto/
├── integrador.py
├── requirements.txt
├── ANALISIS.md
├── salida/
│   ├── normalizadas.json
│   └── reporte.json
└── tests/
```

## Restricciones

No está permitido:

- modificar los datasets;
- modificar respuestas obtenidas de la API;
- sustituir el programa por envíos manuales;
- omitir registros problemáticos sin documentar su resultado;
- alterar el contrato institucional.

Se permite consultar documentación oficial de Python y de las bibliotecas utilizadas.

## Criterios de evaluación

| Criterio | Porcentaje |
|---|---:|
| Análisis de contratos | 10% |
| Lectura y normalización | 20% |
| Validación | 15% |
| Integración HTTP | 20% |
| Manejo de errores y reintentos | 10% |
| Reporte y trazabilidad | 10% |
| Pruebas automatizadas | 10% |
| Calidad y claridad del código | 5% |
| **Total** | **100%** |

## Tiempo

Plazo de desarrollo: **4 días**.
