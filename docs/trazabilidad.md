# Matriz de trazabilidad

La columna "Implementación" ya apunta al código. Faltan por completar las columnas de pull request y de prueba.
Rutas relativas a backend/src/ (backend) y frontend/ (pantallas).

| Condición | Requisito aprobado | Implementación (ruta/componente) | Pull request | Prueba |
|---|---|---|---|---|
| CA-01 | RF-01, RF-02 | POST /api/reportes · endpoints/reportes.py::crear · services/reportes.py::crear_reporte · schemas/reporte.py::ReporteCrear · frontend/templates/solicitante.html · frontend/static/js/solicitante.js | Por completar | Por completar |
| CA-02 | RF-03, RF-06, RF-10 | PATCH /api/reportes/{id}/asignar, /iniciar, /terminar · services/reportes.py · utils/security.py (scopes) · utils/reglas.py · frontend/static/js/coordinador.js, frontend/static/js/tecnico.js | Por completar | Por completar |
| CA-03 | RF-04, RF-08 | GET /api/reportes/{id} · services/reportes.py::obtener_reporte · frontend/static/js/ui.js::renderDetalle | Por completar | Por completar |
| CA-04 | RF-05, RF-07 | POST /api/reportes/{id}/intervenciones, GET /api/reportes/{id}/historial · entities/intervencion.py · frontend/static/js/tecnico.js | Por completar | Por completar |
| CA-05 | RF-08, RF-11 | PATCH /api/reportes/{id}/cerrar (técnico asignado), POST /api/reportes/{id}/calificacion, GET /api/reportes/{id} · frontend/static/js/solicitante.js | Por completar | Por completar |
| CA-06 | RF-09 | GET /api/consolidado · endpoints/consolidado.py · services/reportes.py::consolidado · frontend/static/js/coordinador.js | Por completar | Por completar |