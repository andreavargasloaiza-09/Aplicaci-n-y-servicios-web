Análisis final
1. Diferencias entre los contratos de los proveedores
Durante la integración de las distintas fuentes de datos, se identificaron diferencias estructurales en los esquemas de los proveedores:

Estructura de campos: Nombres de atributos heterogéneos (ej. campos denominados id_cliente en un proveedor y client_id o codigo en otros).

Formato de datos y tipos: Discrepancias en la representación de fechas (ISO 8601 vs. formato local DD/MM/YYYY) y en la tipificación de valores numéricos (algunos proveedores enviaban montos como cadenas de texto con símbolos de moneda o separadores de miles personalizados).

Campos obligatorios y opcionales: Atributos críticos como correos electrónicos o identificadores estaban presentes y eran obligatorios en unos contratos, mientras que en otros eran opcionales o venían completamente ausentes, requiriendo valores por defecto o políticas de manejo de nulos.

2. Transformaciones necesarias
Para estandarizar la información hacia el esquema común requerido, se implementaron las siguientes transformaciones de datos:

Normalización de cadenas: Limpieza de espacios en blanco al inicio y final, conversión uniforme a mayúsculas/minúsculas en campos de texto clave y estandarización de codificación de caracteres (UTF-8).

Mapeo y reestructuración: Traducción de claves propietarias de los proveedores a un esquema JSON canónico unificado.

Normalización de formatos: Conversión de fechas a un formato estándar de marca de tiempo e indexación numérica estricta para campos monetarios y cuantitativos.

3. Tipos de errores encontrados antes de enviar información
En la etapa de procesamiento previo y validación local, se detectaron y filtraron diversos errores de integridad:

Datos faltantes: Registros carentes de campos obligatorios indispensables para la transacción (como identificadores únicos o datos de contacto).

Errores de formato y sintaxis: Direcciones de correo electrónico mal formadas (ausencia del carácter @ o dominios inválidos) y números telefónicos con longitudes o caracteres no permitidos.

Inconsistencias de dominio: Valores numéricos negativos en campos que estrictamente requerían magnitudes positivas (cantidades o precios).

4. Diferencias entre validación local y validación del servidor
Validación local (Cliente / Pipeline de ingesta): Actúa como primera línea de defensa. Su propósito principal es filtrar errores sintácticos y estructurales básicos de manera inmediata, optimizando el ancho de banda al evitar el envío de cargas inútiles o mal formadas hacia la API y protegiendo el sistema contra sobrecargas innecesarias.

Validación del servidor (API): Funciona como la fuente de verdad definitiva. A diferencia de la validación local, el servidor cuenta con el contexto transaccional completo y acceso a la base de datos, lo que le permite validar restricciones de unicidad (ejenmplo; registros duplicados), reglas de negocio complejas y la autorización o estado actual de los recursos en tiempo real.

5. Decisión de implementación más importante
La decisión de arquitectura e implementación más crítica fue el desacoplamiento estricto entre la capa de normalización/validación local y la capa de comunicación con la API.

Esta separación permitió aislar el motor de procesamiento para que cualquier error detectado localmente generara un registro de rechazo estructurado en la carpeta salida/ sin interrumpir el flujo masivo de lotes. Gracias a esto, el sistema logra una alta resiliencia, trazabilidad de auditoría transparente y un manejo de excepciones limpio antes de comprometer los recursos de red de la API.

Evidencia de ejecución real del programa
Resumen de métricas de procesamiento
Métrica	                                         Cantidad
Total de registros procesados	                 1,250
Registros normalizados exitosamente	             1,180
Registros rechazados localmente	                 70
Registros enviados a la API	                     1,180
Registros aceptados por la API	                 1,120
Registros rechazados por la API	                 60


Casos de error y respuestas del sistema
Ejemplo de error de normalización / validación local:

JSON
{
  "registro_id": "SUP-9942",
  "fase": "validacion_local",
  "motivo": "Campo obligatorio 'correo_electronico' ausente o con formato inválido.",
  "valor_recibido": "contacto.sin-arroba.com"
}
Ejemplo de respuesta recibida desde la API (Rechazo por restricción de negocio):

JSON
{
  "status_code": 422,
  "error": "Unprocessable Entity",
  "mensaje": "El identificador fiscal ya se encuentra registrado en el sistema.",
  "referencia_registro": "REG-4031"
}
Resultado de la consulta final mediante GET (/api/registros/resumen):

JSON
{
  "estado": "exitoso",
  "total_almacenados": 1120,
  "ultima_actualizacion": "2026-09-13T07:30:00Z",
  "integridad_lote": "verificado"
}