from fastapi import APIRouter, HTTPException
from models.actuators import ActuatorCommandCreate, ActuatorCommand, ActuatorState, ActuatorStateCreate
import json
from db import db
from mqtt import mqtt_client


router = APIRouter(prefix="/actuators", tags=["actuators"])

@router.post("/commands", response_model=ActuatorCommandCreate)
def create_command(cmd: ActuatorCommandCreate):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actuator_commands (device_id, command, value, issued_by)
        VALUES (%s, %s, %s, %s)
    """, (cmd.device_id, cmd.command, cmd.value, cmd.issued_by))

        # Publicar en MQTT
    topic = f"iot_house_tec/casa/actuator/command/{cmd.device_id}"
    mqtt_client.publish(topic, json.dumps({
        "source": "frontend",
        "type": "command",
        "device_id": cmd.device_id,
        "payload": {
            "action": cmd.command,
            "value": cmd.value
        }
    }))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return ActuatorCommandCreate(**cmd.model_dump())

@router.get("/status", response_model=list[ActuatorState])
def get_actuators_states():
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM actuator_states
    """)

    states = cursor.fetchall()

    cursor.close()
    conn.close()

    if not states:
        raise HTTPException(404, "Actuator states not found")

    return states

@router.get("/{device_id}/status", response_model=ActuatorState)
def get_actuator_state(device_id: int):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM actuator_states
        WHERE device_id = %s
        ORDER BY updated_at DESC
        LIMIT 1
    """, (device_id,))

    state = cursor.fetchone()

    cursor.close()
    conn.close()

    if not state:
        raise HTTPException(404, "Actuator state not found")

    return state

@router.put("/{device_id}", response_model=ActuatorState)
def upsert_actuator_state(device_id: int, body: ActuatorStateCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    # UPSERT: Inserta o actualiza si ya existe
    cursor.execute("""
        INSERT INTO actuator_states (device_id, state)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE 
            state = VALUES(state),
            updated_at = CURRENT_TIMESTAMP
    """, (device_id, body.state))

    conn.commit()

    # Obtener el estado actualizado
    cursor.execute("SELECT * FROM actuator_states WHERE device_id = %s", (device_id,))
    state = cursor.fetchone()

    cursor.close()
    conn.close()

    return state