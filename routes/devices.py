from fastapi import APIRouter, HTTPException
from models.devices import DeviceCreate, Device
from db import db

router = APIRouter(prefix="/devices", tags=["devices"])

# CREATE
@router.post("/", response_model=Device)
def create_device(device: DeviceCreate):
    try:
        conn = db.connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO devices (name, type, model, location, topic)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            device.name,
            device.type,
            device.model,
            device.location,
            device.topic
        ))

        conn.commit()
        new_id = cursor.lastrowid

        return Device(id=new_id, **device.model_dump())

    except Exception as e:
        raise HTTPException(500, f"Error inserting device: {e}")

    finally:
        cursor.close()
        conn.close()


# READ ALL
@router.get("/", response_model=list[Device])
def get_devices():
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    cursor.close()
    conn.close()
    return devices


# READ ONE
@router.get("/{device_id}", response_model=Device)
def get_device(device_id: int):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM devices WHERE id=%s", (device_id,))
    device = cursor.fetchone()

    cursor.close()
    conn.close()

    if not device:
        raise HTTPException(404, "Device not found")

    return device


# UPDATE
@router.put("/{device_id}", response_model=Device)
def update_device(device_id: int, device: DeviceCreate):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE devices
        SET name=%s, type=%s, model=%s, location=%s, topic=%s
        WHERE id=%s
    """, (
        device.name,
        device.type,
        device.model,
        device.location,
        device.topic,
        device_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return Device(id=device_id, **device.dict())


# DELETE
@router.delete("/{device_id}")
def delete_device(device_id: int):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM devices WHERE id=%s", (device_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Device deleted"}