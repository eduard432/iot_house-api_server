from fastapi import APIRouter, HTTPException
from models.actuators import ActuatorCommandCreate, ActuatorCommand, ActuatorState, ActuatorStateCreate
from db import db

router = APIRouter(prefix="/actuators", tags=["actuators"])

@router.post("/commands", response_model=ActuatorCommand)
def create_command(cmd: ActuatorCommandCreate):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actuator_commands (device_id, command, value, issued_by)
        VALUES (%s, %s, %s, %s)
    """, (cmd.device_id, cmd.command, cmd.value, cmd.issued_by))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return ActuatorCommand(id=new_id, **cmd.model_dump())


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

@router.put("/{state_id}", response_model=ActuatorState)
def update_actuator_state(state_id: int, body: ActuatorStateCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    # Verificar que existe
    cursor.execute("SELECT * FROM actuator_states WHERE id = %s", (state_id,))
    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Actuator state not found")

    # Actualizar
    cursor.execute("""
        UPDATE actuator_states
        SET state = %s
        WHERE id = %s
    """, (body.state, state_id))

    conn.commit()

    # Obtener actualizado
    cursor.execute("SELECT * FROM actuator_states WHERE id = %s", (state_id,))
    updated = cursor.fetchone()

    cursor.close()
    conn.close()

    return updated

@router.post("/{device_id}", response_model=ActuatorState)
def create_actuator_state(device_id: int, body: ActuatorStateCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO actuator_states (device_id, state)
        VALUES (%s, %s)
    """, (device_id, body.state))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.execute("SELECT * FROM actuator_states WHERE id=%s", (new_id,))
    state = cursor.fetchone()

    cursor.close()
    conn.close()

    return state