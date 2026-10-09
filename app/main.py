from fastapi import FastAPI
from app.api import medicion  
from app.mqtt.client import start_mqtt_client

app = FastAPI(title="IoT API - Taller 2")

app.include_router(medicion.router, tags=["Mediciones"])

@app.on_event("startup")
async def startup_event():
    print("Iniciando cliente MQTT...")
    start_mqtt_client()