from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.modules.events.models import Event
from app.modules.registrations.models import Registration
from app.modules.users.models import User
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime


class EventService:
    @staticmethod
    def create_event(
        db: Session, event_data: dict, organizer_id: int
    ) -> Event:
        # Validate dates
        if event_data["end_datetime"] <= event_data["start_datetime"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time",
            )

        # Преобразуем HttpUrl в строку, если нужно
        if "image_url" in event_data and event_data["image_url"] is not None:
            if hasattr(event_data["image_url"], "__str__"):
                event_data["image_url"] = str(event_data["image_url"])

        db_event = Event(**event_data, organizer_id=organizer_id)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Event:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        return event

    @staticmethod
    def update_event(
        db: Session, event_id: int, update_data: dict, organizer_id: int
    ) -> Event:
        event = EventService.get_event_by_id(db, event_id)

        # Check if user is organizer
        if event.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the organizer can update this event",
            )

        # Преобразуем HttpUrl в строку, если нужно
        if "image_url" in update_data and update_data["image_url"] is not None:
            if hasattr(update_data["image_url"], "__str__"):
                update_data["image_url"] = str(update_data["image_url"])

        # Update fields
        for key, value in update_data.items():
            if value is not None:
                setattr(event, key, value)

        # Auto-update status based on dates
        now = datetime.now()
        if event.end_datetime < now:
            event.status = "past"
        elif event.start_datetime > now:
            event.status = "upcoming"

        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def delete_event(db: Session, event_id: int, organizer_id: int):
        event = EventService.get_event_by_id(db, event_id)

        if event.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the organizer can delete this event",
            )

        db.delete(event)
        db.commit()

    @staticmethod
    def get_organizer_events(
        db: Session, organizer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        return (
            db.query(Event)
            .filter(Event.organizer_id == organizer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_public_events(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        status: Optional[str] = None,
        start_from: Optional[datetime] = None,
        start_to: Optional[datetime] = None,
        search: Optional[str] = None,
        location: Optional[str] = None,
    ) -> List[Event]:
        query = db.query(Event).filter(Event.status != "cancelled")

        if category:
            query = query.filter(Event.category == category)

        if status:
            query = query.filter(Event.status == status)

        if start_from:
            query = query.filter(Event.start_datetime >= start_from)

        if start_to:
            query = query.filter(Event.start_datetime <= start_to)

        if location:
            query = query.filter(Event.location.ilike(f"%{location}%"))

        if search:
            query = query.filter(
                or_(
                    Event.title.ilike(f"%{search}%"),
                    Event.description.ilike(f"%{search}%"),
                    Event.location.ilike(f"%{search}%"),
                )
            )

        return (
            query.order_by(Event.start_datetime)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_events_with_registration_counts(
        db: Session, query, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get events with pre-calculated registration counts"""
        # Подзапрос для подсчета регистраций
        registration_count_subq = (
            select(Registration.event_id, func.count().label("reg_count"))
            .group_by(Registration.event_id)
            .subquery()
        )

        # Основной запрос с присоединением подсчета
        events_with_counts = (
            query.outerjoin(
                registration_count_subq,
                Event.id == registration_count_subq.c.event_id,
            )
            .add_columns(
                func.coalesce(registration_count_subq.c.reg_count, 0).label(
                    "registered_count"
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        result = []
        for event, registered_count in events_with_counts:
            # Преобразуем в словарь с дополнительным полем
            event_dict = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "image_url": event.image_url,
                "start_datetime": event.start_datetime,
                "end_datetime": event.end_datetime,
                "location": event.location,
                "category": event.category,
                "max_participants": event.max_participants,
                "status": event.status,
                "organizer_id": event.organizer_id,
                "created_at": event.created_at,
                "registered_count": registered_count,
                "available_spots": event.max_participants - registered_count
                if event.max_participants
                else None,
            }
            result.append(event_dict)

        return result

    @staticmethod
    def get_organizer_events_with_counts(
        db: Session, organizer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get organizer's events with registration counts"""
        query = db.query(Event).filter(Event.organizer_id == organizer_id)
        return EventService.get_events_with_registration_counts(
            db, query, skip, limit
        )

    @staticmethod
    def get_public_events_with_counts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        status: Optional[str] = None,
        start_from: Optional[datetime] = None,
        start_to: Optional[datetime] = None,
        search: Optional[str] = None,
        location: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get public events with registration counts"""
        query = db.query(Event).filter(Event.status != "cancelled")

        if category:
            query = query.filter(Event.category == category)

        if status:
            query = query.filter(Event.status == status)

        if start_from:
            query = query.filter(Event.start_datetime >= start_from)

        if start_to:
            query = query.filter(Event.start_datetime <= start_to)

        if location:
            query = query.filter(Event.location.ilike(f"%{location}%"))

        if search:
            query = query.filter(
                or_(
                    Event.title.ilike(f"%{search}%"),
                    Event.description.ilike(f"%{search}%"),
                    Event.location.ilike(f"%{search}%"),
                )
            )

        query = query.order_by(Event.start_datetime)
        return EventService.get_events_with_registration_counts(
            db, query, skip, limit
        )

    @staticmethod
    def get_event_registered_count(db: Session, event_id: int) -> int:
        return (
            db.query(Registration)
            .filter(Registration.event_id == event_id)
            .count()
        )

    @staticmethod
    def get_event_participants(db: Session, event_id: int) -> List[User]:
        return (
            db.query(User)
            .join(Registration)
            .filter(Registration.event_id == event_id)
            .all()
        )
