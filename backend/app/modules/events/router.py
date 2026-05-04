from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import (
    get_current_organizer,
    get_current_user,
    get_optional_user,
)
from app.modules.events.schemas import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventWithDetails,
    EventFilter,
)
from app.modules.events.models import Event
from app.modules.events.service import EventService
from app.modules.users.models import User
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=201)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Create a new event (organizer only)"""
    return EventService.create_event(db, event_data.dict(), current_user.id)


@router.get("/", response_model=List[EventWithDetails])
def get_public_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    start_from: Optional[datetime] = None,
    start_to: Optional[datetime] = None,
    search: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Get public events with pagination and filtering"""
    # Используем оптимизированный метод
    events_with_counts = EventService.get_public_events_with_counts(
        db,
        skip,
        limit,
        category,
        status,
        start_from,
        start_to,
        search,
        location,
    )

    # Преобразуем в объекты EventWithDetails
    result = []
    for event_data in events_with_counts:
        result.append(EventWithDetails(**event_data))

    return result


@router.get("/my-events", response_model=List[EventWithDetails])
def get_my_events(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get events created by current user (organizer) with registered_count"""
    # Используем оптимизированный метод
    events_with_counts = EventService.get_organizer_events_with_counts(
        db, current_user.id, skip, limit
    )

    # Преобразуем в объекты EventWithDetails
    result = []
    for event_data in events_with_counts:
        result.append(EventWithDetails(**event_data))

    return result


@router.get("/{event_id}", response_model=EventWithDetails)
def get_event_details(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Get detailed event information"""
    # Для одного события можно использовать простой метод или оптимизированный
    event = EventService.get_event_by_id(db, event_id)
    registered_count = EventService.get_event_registered_count(db, event.id)
    available_spots = (
        event.max_participants - registered_count
        if event.max_participants
        else None
    )

    return EventWithDetails(
        **event.__dict__,
        registered_count=registered_count,
        available_spots=available_spots,
    )


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    update_data: EventUpdate,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Update event (organizer only)"""
    return EventService.update_event(
        db, event_id, update_data.dict(exclude_unset=True), current_user.id
    )


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Delete event (organizer only)"""
    EventService.delete_event(db, event_id, current_user.id)
    return {"message": "Event deleted successfully"}


@router.get("/{event_id}/participants", response_model=List[dict])
def get_event_participants(
    event_id: int,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Get list of participants registered for an event (organizer only)"""
    event = EventService.get_event_by_id(db, event_id)

    # Check if user is the organizer
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only the organizer can view participants"
        )

    participants = EventService.get_event_participants(db, event_id)
    return [
        {"id": p.id, "name": p.name, "email": p.email} for p in participants
    ]
