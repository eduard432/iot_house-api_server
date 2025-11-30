from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActuatorCommandBase(BaseModel):
    device_id: int
    command: str
    value: Optional[str] = None
    issued_by: Optional[str] = None

class ActuatorCommandCreate(ActuatorCommandBase):
    pass

class ActuatorCommand(ActuatorCommandBase):
    id: int
    created_at: datetime

class ActuatorStateBase(BaseModel):
    state: str

class ActuatorStateCreate(ActuatorStateBase):
    device_id: int
    pass

class ActuatorState(ActuatorStateBase):
    updated_at: datetime