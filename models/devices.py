from pydantic  import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    type: str  # sensor | actuator
    model: Optional[str] = None
    location: Optional[str] = None
    topic: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    created_at: datetime
