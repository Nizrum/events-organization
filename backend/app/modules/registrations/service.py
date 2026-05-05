from sqlalchemy.orm import Session
from app.modules.registrations.models import Registration
from app.modules.events.models import Event
from app.modules.events.service import EventService
from fastapi import HTTPException, status
from typing import List


class RegistrationService:
    @staticmethod
    def register_for_event(
        db: Session, user_id: int, event_id: int
    ) -> Registration:
        # Check if event exists
        event = EventService.get_event_by_id(db, event_id)

        # Check if event is cancelled
        if event.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot register for cancelled event",
            )

        # Check if already registered
        existing = (
            db.query(Registration)
            .filter(
                Registration.user_id == user_id,
                Registration.event_id == event_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already registered for this event",
            )

        # Check capacity
        registered_count = EventService.get_event_registered_count(
            db, event_id
        )
        if (
            event.max_participants
            and registered_count >= event.max_participants
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Event is full"
            )

        # Create registration
        registration = Registration(user_id=user_id, event_id=event_id)
        db.add(registration)
        db.commit()
        db.refresh(registration)

        return registration

    @staticmethod
    def cancel_registration(db: Session, user_id: int, event_id: int):
        registration = (
            db.query(Registration)
            .filter(
                Registration.user_id == user_id,
                Registration.event_id == event_id,
            )
            .first()
        )

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found",
            )

        db.delete(registration)
        db.commit()

    @staticmethod
    def get_user_registrations(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        """Get events user is registered for with pagination"""
        return (
            db.query(Event)
            .join(Registration)
            .filter(Registration.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def is_registered(db: Session, user_id: int, event_id: int) -> bool:
        return (
            db.query(Registration)
            .filter(
                Registration.user_id == user_id,
                Registration.event_id == event_id,
            )
            .first()
            is not None
        )
