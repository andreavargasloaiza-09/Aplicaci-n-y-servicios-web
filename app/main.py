from fastapi import FastAPI
from app.api import medicion, sensor, sensor_magnitud
from app.mqtt.client import start_mqtt_client

app = FastAPI(title="IoT API - Taller 2")

# Registrar todos los controladores
app.include_router(sensor.router)
app.include_router(sensor_magnitud.router)
app.include_router(medicion.router)

@app.on_event("startup")
async def startup_event():
    print("Iniciando cliente MQTT...")
    start_mqtt_client()