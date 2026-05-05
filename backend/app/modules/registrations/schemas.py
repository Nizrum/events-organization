from pydantic import BaseModel
from datetime import datetime


class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    registration_date: datetime

    class Config:
        from_attributes = True


class RegistrationCreate(BaseModel):
    event_id: int
