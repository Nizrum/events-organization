from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.registrations.schemas import (
    RegistrationResponse,
    RegistrationCreate,
)
from app.modules.registrations.service import RegistrationService
from app.modules.events.schemas import EventWithDetails
from app.modules.events.service import EventService
from app.modules.users.models import User

router = APIRouter()


@router.post("/", response_model=RegistrationResponse, status_code=201)
def register_for_event(
    registration_data: RegistrationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Register for an event"""
    registration = RegistrationService.register_for_event(
        db, current_user.id, registration_data.event_id
    )
    return registration


@router.delete("/{event_id}")
def cancel_registration(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel registration for an event"""
    RegistrationService.cancel_registration(db, current_user.id, event_id)
    return {"message": "Registration cancelled successfully"}


@router.get("/my-events", response_model=List[EventWithDetails])
def get_my_registered_events(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all events the current user is registered for with registered_count"""
    # Получаем события, на которые зарегистрирован пользователь
    events = RegistrationService.get_user_registrations(
        db, current_user.id, skip, limit
    )

    # Для каждого события получаем количество регистраций
    # Здесь можно также оптимизировать, но для регистраций пользователя
    # обычно не так много событий, поэтому можно оставить как есть
    result = []
    for event in events:
        registered_count = EventService.get_event_registered_count(
            db, event.id
        )
        available_spots = (
            event.max_participants - registered_count
            if event.max_participants
            else None
        )

        result.append(
            EventWithDetails(
                **event.__dict__,
                registered_count=registered_count,
                available_spots=available_spots,
            )
        )

    return result


@router.get("/check/{event_id}")
def check_registration(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if current user is registered for an event"""
    is_registered = RegistrationService.is_registered(
        db, current_user.id, event_id
    )
    return {"registered": is_registered}
