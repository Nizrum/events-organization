from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, List
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None  # Изменено с HttpUrl на str
    start_datetime: datetime
    end_datetime: datetime
    location: str
    category: Optional[str] = None
    max_participants: Optional[int] = None

    @field_validator("image_url", mode="before")
    @classmethod
    def validate_image_url(cls, v):
        if v is None:
            return None
        # Если это HttpUrl объект, преобразуем в строку
        if hasattr(v, "scheme") and hasattr(v, "host"):
            return str(v)
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None  # Изменено с HttpUrl на str
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    category: Optional[str] = None
    max_participants: Optional[int] = None
    status: Optional[str] = None


class EventResponse(EventBase):
    id: int
    status: str
    organizer_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EventWithDetails(EventResponse):
    registered_count: int = 0
    available_spots: Optional[int] = None


class EventFilter(BaseModel):
    category: Optional[str] = None
    status: Optional[str] = None
    start_from: Optional[datetime] = None
    start_to: Optional[datetime] = None
    search: Optional[str] = None
    location: Optional[str] = None
