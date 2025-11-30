from models.sensors import SensorReadingCreate
from db import db

def save_sensor_reading(data: SensorReadingCreate):
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    query = """
    INSERT INTO sensor_readings (device_sensor_id, value)
    VALUES (%s, %s)
    """
    cursor.execute(query, (data.device_sensor_id, data.value))
    conn.commit()

    new_id = cursor.lastrowid

    cursor.execute("SELECT * FROM sensor_readings WHERE id = %s", (new_id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return item