# Mesa de servicios de soporte tecnológico

> Proyecto Final PF-02 — Aplicaciones y Servicios Web — Tecnología en Desarrollo de Software

## 1. Información general
- Integrantes y contribución de cada uno: (completar)
- Asignatura / fecha / repositorio: (completar)

## 2. Descripción del sistema
(completar; enlazar docs/requisitos.md)

## 3. Requisitos y alcance
(completar: método, evidencia de la entrevista, decisiones del docente)

## 4. Arquitectura, diseño de API y modelo de datos
(completar; enlazar docs/diseno.md)

### Tecnologías y justificación
- *Backend:* Python + FastAPI. API REST con autenticación JWT y permisos por scopes.
- *Frontend:* FastAPI con plantillas *Jinja2* (las pantallas) y *JavaScript* que consume la API REST. Es una sola aplicación y se ejecuta con un solo comando. El frontend sigue separado de la lógica de negocio: las pantallas solo entregan HTML y todos los datos viajan por la API REST, que verifica los permisos en cada solicitud.
- *Base de datos:* relacional, con SQLAlchemy. SQLite por defecto; se cambia con DATABASE_URL.

### Organización del código

backend/src/
├── endpoints/   Rutas HTTP: reciben la solicitud, verifican permisos y responden
├── services/    Lógica de los casos y registro del historial
├── entities/    Tablas de la base de datos (usuarios, categorías, reportes, intervenciones)
├── schemas/     Validación de lo que entra y sale de la API
├── database/    Conexión y sesión de la base de datos
├── utils/       Reglas del negocio (reglas.py), seguridad (JWT y scopes) y configuración
└── main.py      Arma la aplicación FastAPI

frontend/
├── templates/   Pantallas (Jinja2): base, ingreso, solicitante, técnico y coordinación
└── static/      CSS y JavaScript (api.js habla con la API; ui.js dibuja; uno por pantalla)


## 5. Configuración del entorno

Requisitos: Python 3.10 o superior.

bash
# 1. Entorno virtual e instalación (desde la raíz del repositorio)
python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Variables de entorno
cp .env.example .env               # En Windows: copy .env.example .env
# Edite .env: reemplace SECRET_KEY por una clave generada con
#   python -c "import secrets; print(secrets.token_urlsafe(48))"
# y escriba en DEMO_PASSWORD la clave de prueba que usarán los usuarios ficticios.

# 3. Base de datos y datos ficticios de prueba (desde backend/)
cd backend
python seed.py

# 4. Ejecutar (desde backend/)
uvicorn src.main:app --reload


- Aplicación web: <http://127.0.0.1:8000/>
- Documentación interactiva de la API: <http://127.0.0.1:8000/docs>

Usuarios ficticios (todos usan la clave que definan en DEMO_PASSWORD dentro de su .env):

| Rol | Correo |
|---|---|
| Coordinador | coordinador@demo.test |
| Técnico | tecnico1@demo.test, tecnico2@demo.test |
| Solicitante | solicitante1@demo.test, solicitante2@demo.test |

Para reiniciar los datos de prueba: python seed.py --reset (desde backend/).

### Errores frecuentes al arrancar

| Mensaje | Causa y solución |
|---|---|
| No module named 'app' | Se usó el comando antiguo. El correcto es uvicorn src.main:app --reload |
| No module named 'src' | La terminal no está en backend/. Ejecute cd backend primero |
| SECRET_KEY o DEMO_PASSWORD faltante | Falta esa línea en el .env de la raíz del repositorio |
| No module named 'jinja2' (u otro paquete) | Ejecute pip install -r requirements.txt con el entorno virtual activo |

## 6. Servicios web implementados

Documentación interactiva: /docs. Todas las rutas, salvo el inicio de sesión, exigen el token JWT.

| Método | Ruta | Descripción | Requisito relacionado |
|---|---|---|---|
| POST | /api/auth/login | Inicia sesión y devuelve el token con sus scopes | RF-10 |
| GET | /api/auth/me | Usuario de la sesión actual | RF-10 |
| GET | /api/categorias | Lista las categorías | RF-02 |
| GET | /api/usuarios/tecnicos | Lista los técnicos (solo coordinación) | RF-03 |
| POST | /api/reportes | Reporta un caso | RF-01, RF-02 |
| GET | /api/reportes | Lista los casos que el rol puede ver | RF-08, RF-09 |
| GET | /api/reportes/{id} | Detalle: estado, responsable, resultado | RF-08 |
| GET | /api/reportes/{id}/historial | Historial de intervenciones en orden | RF-05 |
| PATCH | /api/reportes/{id}/asignar | Asigna técnico (solo coordinación) | RF-03, RF-04 |
| PATCH | /api/reportes/{id}/iniciar | Inicia la reparación (técnico asignado) | RF-06 |
| POST | /api/reportes/{id}/intervenciones | Registra una intervención (técnico asignado) | RF-05 |
| PATCH | /api/reportes/{id}/terminar | Termina con su respuesta (técnico asignado) | RF-06 |
| PATCH | /api/reportes/{id}/cerrar | Cierra el caso (técnico asignado); no se reabre | RN-05, RF-07 |
| POST | /api/reportes/{id}/calificacion | Califica un caso cerrado (solicitante) | RF-11 |
| GET | /api/consolidado | Casos abiertos y cerrados con estado y responsable | RF-09 |

Códigos de respuesta: 200/201 éxito · 401 sin sesión válida · 403 sin permiso · 404 no existe · 409 acción no válida para el estado del caso · 422 datos inválidos.

(completar con ejemplos de solicitudes y respuestas tomados de las pruebas)

## 7. Pruebas de API e integración y evidencias
(completar; evidencias en evidencias/; enlazar docs/trazabilidad.md)

## 8. Control de versiones
(completar: pull requests relevantes y aportes de cada integrante)

## 9. Conclusiones y limitaciones
(completar)