from fastapi import APIRouter, HTTPException
from models.actuators import ActuatorStateCreate

from db import db

def save_actuator_state(data: ActuatorStateCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    # UPSERT: Inserta o actualiza si ya existe
    cursor.execute("""
        INSERT INTO actuator_states (device_id, state)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE 
            state = VALUES(state),
            updated_at = CURRENT_TIMESTAMP
    """, (data.device_id, data.state))

    conn.commit()

    # Obtener el estado actualizado
    cursor.execute("SELECT * FROM actuator_states WHERE device_id = %s", (data.device_id,))
    state = cursor.fetchone()

    cursor.close()
    conn.close()

    return state