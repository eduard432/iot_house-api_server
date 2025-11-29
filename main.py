from fastapi import FastAPI
from routes.devices import router as devices_router
from routes.sensors import router as sensors_router
from routes.actuators import router as actuators_router

app = FastAPI()

app.include_router(devices_router)
app.include_router(sensors_router)
app.include_router(actuators_router)

@app.get("/")
def root():
    return {"message": "Casa IoT API lista 🚀"}
