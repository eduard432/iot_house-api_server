import paho.mqtt.client as mqtt
import asyncio
import json

# Controladores (asume que los tienes)
from controllers.sensors import save_sensor_reading
from controllers.actuators import save_actuator_state

ws_clients = []
main_loop = asyncio.get_event_loop()

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT conectado:", rc)
    client.subscribe("iot_house_tec/casa/#")

def on_message(client, userdata, msg):
    topic: str = msg.topic
    raw = msg.payload.decode()

    try:
        message = json.loads(raw)
    except:
        print("Mensaje inválido")
        return

    print("MQTT recibió:", topic, message)

    # ---------------------------------------------------------
    # 1. SENSOR DATA  -----------------------------------------
    # ---------------------------------------------------------
    # Topic esperado:
    # iot_house_tec/casa/sensor/data/<device_id>
    if topic.startswith("iot_house_tec/casa/sensor/data/"):

        device_id = topic.split("/")[-1]  # extrae <device_id>
        payload = message.get("payload", {})

        # Guardar *cada* sensor_id individualmente
        for device_sensor_id, value in payload.items():

            reading_data = {
                "device_id": device_id,
                "device_sensor_id": device_sensor_id,
                "value": value
            }

            # Guardar en la DB
            save_sensor_reading(reading_data)

            # Notificar al frontend un evento por sensor
            normalized_msg = {
                "type": "sensor_reading",
                "device_id": device_id,
                "sensor_id": device_sensor_id,
                "value": value
            }

            for ws in ws_clients:
                main_loop.create_task(ws.send_text(json.dumps(normalized_msg)))

        return  # evita procesar como otro tipo


    # ---------------------------------------------------------
    # 2. ACTUATOR STATE  --------------------------------------
    # ---------------------------------------------------------
    # Topic esperado:
    # iot_house_tec/casa/actuator/state/<device_id>
    if topic.startswith("iot_house_tec/casa/actuator/state/"):

        device_id = topic.split("/")[-1]
        state = message.get("payload", {}).get("state")

        if state is not None:
            # Guardar en la DB
            save_actuator_state({
                "device_id": device_id,
                "state": state
            })

        # Notificar exactamente lo que llegó
        for ws in ws_clients:
            main_loop.create_task(ws.send_text(json.dumps({
                "type": "actuator_state",
                "device_id": device_id,
                "state": state
            })))

        return


    # ---------------------------------------------------------
    # 3. OTROS TIPOS DE MENSAJE (si los agregas a futuro)
    # ---------------------------------------------------------

    # Enviar mensaje genérico al frontend si no entró en los casos anteriores
    for ws in ws_clients:
        main_loop.create_task(ws.send_text(json.dumps({
            "topic": topic,
            "message": message
        })))



mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("test.mosquitto.org", 1883)
mqtt_client.loop_start()
