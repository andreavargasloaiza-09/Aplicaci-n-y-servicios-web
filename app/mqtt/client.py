import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
from pydantic import ValidationError
from app.schemas.medicion import MQTTPayload
from app.database.connection import SessionLocal
from app.models.sensor import Sensor
from app.models.sensor_magnitud import SensorMagnitud
from app.models.medicion import Medicion

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "iot/sensors/+/data")

def procesar_mensaje(payload_str: str, topic: str):
    db = SessionLocal()
    try:
        # 1. Validación Pydantic
        data = json.loads(payload_str)
        payload = MQTTPayload(**data)
        
        # 2. Validar Existencia y Estado del Sensor
        sensor = db.query(Sensor).filter(Sensor.codigo == payload.sensor_id).first()
        if not sensor or not sensor.activo:
            print(f"Rechazado: Sensor {payload.sensor_id} no existe o inactivo.")
            return
        
        nuevas_mediciones = []
        # 3. Validar Magnitudes y Unidades
        for mag_nombre, mag_data in payload.measurements.items():
            magnitud_db = db.query(SensorMagnitud).filter(
                SensorMagnitud.sensor_id == sensor.id,
                SensorMagnitud.magnitud == mag_nombre
            ).first()
            
            if not magnitud_db:
                print(f"Rechazado: Magnitud {mag_nombre} no asociada al sensor.")
                return # Si una es inválida se rechaza todo
                
            if magnitud_db.unidad != mag_data.unit:
                print(f"Rechazado: Unidad incorrecta para {mag_nombre}. Esperada {magnitud_db.unidad}")
                return
                
            if not (magnitud_db.valor_minimo <= mag_data.value <= magnitud_db.valor_maximo):
                print(f"Rechazado: Valor {mag_data.value} fuera de rango para {mag_nombre}.")
                return
                
            # Crear objeto de medición
            nueva_medicion = Medicion(
                sensor_magnitud_id=magnitud_db.id,
                valor=mag_data.value,
                timestamp_utc=payload.timestamp
            )
            nuevas_mediciones.append(nueva_medicion)
            
        # 4. Almacenar si todo es valido
        if nuevas_mediciones:
            db.add_all(nuevas_mediciones)
            db.commit()
            print(f"Guardado: {len(nuevas_mediciones)} mediciones del sensor {payload.sensor_id}")
            
    except ValidationError as e:
        print(f"Rechazado: Error de validación Pydantic: {e}")
    except json.JSONDecodeError:
        print("Rechazado: JSON inválido")
    finally:
        db.close()

def on_message(client, userdata, message):
    try:
        payload_str = message.payload.decode("utf-8")
        procesar_mensaje(payload_str, message.topic)
    except Exception as e:
        print(f"Error procesando mensaje MQTT: {e}")

def start_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_start()