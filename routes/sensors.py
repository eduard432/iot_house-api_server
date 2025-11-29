from fastapi import APIRouter, HTTPException, Query
from models.sensors import SensorTypeCreate, SensorType, DeviceSensorCreate, DeviceSensor, SensorReading, SensorReadingCreate
from db import db

router = APIRouter(prefix="/sensors", tags=["sensors"])

# SENSOR TYPES ADMIN CRUD

@router.post("/types", response_model=SensorType)
def create_sensor_type(sensor: SensorTypeCreate):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_types (name, unit, description)
        VALUES (%s, %s, %s)
    """, (sensor.name, sensor.unit, sensor.description))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return SensorType(id=new_id, **sensor.model_dump())


@router.get("/types", response_model=list[SensorType])
def list_sensor_types():
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sensor_types")
    items = cursor.fetchall()

    cursor.close()
    conn.close()
    return items


# DEVICE ↔ SENSOR linking

@router.post("/assign", response_model=DeviceSensor)
def assign_sensor(data: DeviceSensorCreate):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO device_sensors (device_id, sensor_type_id)
        VALUES (%s, %s)
    """, (data.device_id, data.sensor_type_id))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return DeviceSensor(id=new_id, **data.model_dump())

# SENSOR DATA CRUD

@router.get("/{device_sensor_id}/readings", response_model=list[SensorReading])
def get_sensor_readings(device_sensor_id: int, limit: int = Query(default=100, ge=1, le=1000)):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sensor_readings WHERE device_sensor_id = %s ORDER BY recorded_at DESC LIMIT %s", (device_sensor_id, limit,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


@router.get("/{device_sensor_id}/readings/last", response_model=SensorReading)
def get_last_sensor_reading(device_sensor_id: int):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sensor_readings WHERE device_sensor_id = %s ORDER BY recorded_at DESC LIMIT 1", (device_sensor_id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="No readings found for this sensor")

    return item

# CREATE SENSOR READING
@router.post("/readings", response_model=SensorReading)
def create_sensor_reading(payload: SensorReadingCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    query = """
    INSERT INTO sensor_readings (device_sensor_id, value)
    VALUES (%s, %s)
    """
    cursor.execute(query, (payload.device_sensor_id, payload.value))
    conn.commit()

    new_id = cursor.lastrowid

    cursor.execute("SELECT * FROM sensor_readings WHERE id = %s", (new_id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return item