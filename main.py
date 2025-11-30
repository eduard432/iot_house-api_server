from fastapi import FastAPI, WebSocket
import asyncio

# Importamos los routers
from routes.devices import router as devices_router
from routes.sensors import router as sensors_router
from routes.actuators import router as actuators_router

# Importamos MQTT y la lista global de WebSockets
from mqtt import mqtt_client, ws_clients

app = FastAPI()

# -------------------------------
# WebSocket: solo envío de estados, no recibe comandos
# -------------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    ws_clients.append(ws)
    print("WebSocket conectado")

    try:
        # Mantener conexión abierta sin recibir nada del cliente
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print("WebSocket error:", e)

    finally:
        if ws in ws_clients:
            ws_clients.remove(ws)
            print("WebSocket desconectado")


# -------------------------------
# Rutas REST
# -------------------------------
app.include_router(devices_router)
app.include_router(sensors_router)
app.include_router(actuators_router)


@app.get("/")
def root():
    return {"message": "Casa IoT API lista 🚀"}
