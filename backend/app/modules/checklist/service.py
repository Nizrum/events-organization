from sqlalchemy.orm import Session, joinedload
from app.modules.checklist.models import ChecklistItem, ChecklistAssignment
from app.modules.users.models import User
from app.modules.events.service import EventService
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any


class ChecklistService:
    @staticmethod
    def create_checklist_item(
        db: Session, event_id: int, item_data: dict, organizer_id: int
    ) -> ChecklistItem:
        # Check if user is organizer of the event
        event = EventService.get_event_by_id(db, event_id)
        if event.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the event organizer can manage checklist items",
            )

        db_item = ChecklistItem(**item_data, event_id=event_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def update_checklist_item(
        db: Session, item_id: int, update_data: dict, organizer_id: int
    ) -> ChecklistItem:
        item = (
            db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checklist item not found",
            )

        # Check if user is organizer of the event
        event = EventService.get_event_by_id(db, item.event_id)
        if event.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the event organizer can update checklist items",
            )

        for key, value in update_data.items():
            if value is not None:
                setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_checklist_item(db: Session, item_id: int, organizer_id: int):
        item = (
            db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checklist item not found",
            )

        # Check if user is organizer of the event
        event = EventService.get_event_by_id(db, item.event_id)
        if event.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the event organizer can delete checklist items",
            )

        db.delete(item)
        db.commit()

    @staticmethod
    def get_event_checklist(db: Session, event_id: int) -> List[ChecklistItem]:
        return (
            db.query(ChecklistItem)
            .filter(ChecklistItem.event_id == event_id)
            .all()
        )

    @staticmethod
    def get_item_assignments_with_users(
        db: Session, item_id: int
    ) -> List[Dict[str, Any]]:
        """Get assignments with user information for a specific checklist item"""
        assignments = (
            db.query(ChecklistAssignment)
            .filter(ChecklistAssignment.checklist_item_id == item_id)
            .all()
        )

        result = []
        for assignment in assignments:
            user = db.query(User).filter(User.id == assignment.user_id).first()
            result.append(
                {
                    "id": assignment.id,
                    "checklist_item_id": assignment.checklist_item_id,
                    "user_id": assignment.user_id,
                    "user_name": user.name if user else "Unknown",
                    "assigned_at": assignment.assigned_at,
                }
            )
        return result

    @staticmethod
    def assign_item_to_user(
        db: Session, item_id: int, user_id: int
    ) -> ChecklistAssignment:
        item = (
            db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checklist item not found",
            )

        # Check if item is already taken (for single type)
        if item.type == "single":
            existing = (
                db.query(ChecklistAssignment)
                .filter(ChecklistAssignment.checklist_item_id == item_id)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This item is already taken by another user",
                )

        # Check if user already has this item
        user_assignment = (
            db.query(ChecklistAssignment)
            .filter(
                ChecklistAssignment.checklist_item_id == item_id,
                ChecklistAssignment.user_id == user_id,
            )
            .first()
        )

        if user_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have this item assigned",
            )

        assignment = ChecklistAssignment(
            checklist_item_id=item_id, user_id=user_id
        )
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def remove_item_from_user(db: Session, item_id: int, user_id: int):
        assignment = (
            db.query(ChecklistAssignment)
            .filter(
                ChecklistAssignment.checklist_item_id == item_id,
                ChecklistAssignment.user_id == user_id,
            )
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You don't have this item assigned",
            )

        db.delete(assignment)
        db.commit()

    @staticmethod
    def get_user_items_for_event(
        db: Session, user_id: int, event_id: int
    ) -> List[ChecklistItem]:
        return (
            db.query(ChecklistItem)
            .join(ChecklistAssignment)
            .filter(
                ChecklistAssignment.user_id == user_id,
                ChecklistItem.event_id == event_id,
            )
            .all()
        )
