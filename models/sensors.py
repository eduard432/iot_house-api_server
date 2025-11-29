from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorTypeBase(BaseModel):
    name: str
    unit: Optional[str] = None
    description: Optional[str] = None

class SensorTypeCreate(SensorTypeBase):
    pass

class SensorType(SensorTypeBase):
    id: int


class DeviceSensorBase(BaseModel):
    device_id: int
    sensor_type_id: int

class DeviceSensorCreate(DeviceSensorBase):
    pass

class DeviceSensor(DeviceSensorBase):
    id: int

class SensorReadingBase(BaseModel):
    device_sensor_id: int
    value: float

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReading(SensorReadingBase):
    id: int
    recorded_at: datetime