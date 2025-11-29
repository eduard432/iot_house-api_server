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
    device_id: int
    state: str

class ActuatorStateCreate(ActuatorStateBase):
    pass

class ActuatorState(ActuatorStateBase):
    id: int
    updated_at: datetime