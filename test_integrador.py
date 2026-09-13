import pytest
from integrador import normalizar_a, validar_registro

# 1. Prueba de transformación correcta
def test_transformacion_correcta():
    registro_ejemplo = {
        "provider_record_id": "A-001",
        "station": {"code": "STA-02", "city_name": "Medellin", "country_code": "CO"},
        "location": {"lat": 6.242282, "lon": -75.595933},
        "measurements": {
            "temperature_f": 68.0,
            "relative_humidity": 50.0,
            "wind_speed_ms": 5.0
        },
        "observed_at": "2026-09-01T00:00:00-05:00",
        "source": "weather_provider_a"
    }
    resultado, id_reg, error = normalizar_a(registro_ejemplo)
    assert error is None
    assert resultado["ciudad"] == "Medellin"
    assert resultado["pais"] == "CO"

# 2. Prueba de conversión de unidades (Fahrenheit a Celsius y mph a km/h)
def test_conversion_unidades():
    registro_ejemplo = {
        "provider_record_id": "A-002",
        "station": {"code": "STA-02", "city_name": "Cali", "country_code": "CO"},
        "location": {"lat": 3.4516, "lon": -76.532},
        "measurements": {
            "temperature_f": 32.0,  # 32°F deben ser 0°C
            "relative_humidity": 60.0,
            "wind_speed_ms": 10.0   # 10 m/s * 3.6 = 36 km/h
        },
        "observed_at": "2026-09-01T00:00:00-05:00",
        "source": "weather_provider_a"
    }
    resultado, _, _ = normalizar_a(registro_ejemplo)
    assert round(resultado["temperatura_c"], 1) == 0.0
    assert round(resultado["viento_kmh"], 1) == 36.0

# 3. Prueba de un registro válido
def test_registro_valido():
    registro_normalizado = {
        "ciudad": "Medellin",
        "pais": "CO",
        "latitud": 6.24,
        "longitud": -75.59,
        "temperatura_c": 24.5,
        "humedad": 55.0,
        "viento_kmh": 12.0,
        "fecha_hora": "2026-09-01T00:00:00-05:00",
        "origen": "proveedor_a"
    }
    es_valido, motivo = validar_registro(registro_normalizado)
    assert es_valido is True
    assert motivo is None

# 4. Prueba de un registro inválido (ejemplo: humedad fuera de rango, etc...)
def test_registro_invalido():
    registro_normalizado = {
        "ciudad": "Medellin",
        "pais": "CO",
        "latitud": 6.24,
        "longitud": -75.59,
        "temperatura_c": 24.5,
        "humedad": 150.0,  # Inválido (> 100)
        "viento_kmh": 12.0,
        "fecha_hora": "2026-09-01T00:00:00-05:00",
        "origen": "proveedor_a"
    }
    es_valido, motivo = validar_registro(registro_normalizado)
    assert es_valido is False
    assert motivo is not None

# 5. Caso límite seleccionado por el equipo (latitud en el límite exacto de 90°)
def test_caso_limite_latitud():
    registro_limite = {
        "ciudad": "Polo Norte",
        "pais": "GL",
        "latitud": 90.0,  # Límite exacto permitido
        "longitud": 0.0,
        "temperatura_c": -10.0,
        "humedad": 80.0,
        "viento_kmh": 5.0,
        "fecha_hora": "2026-09-01T00:00:00-05:00",
        "origen": "proveedor_a"
    }
    es_valido, _ = validar_registro(registro_limite)
    assert es_valido is True