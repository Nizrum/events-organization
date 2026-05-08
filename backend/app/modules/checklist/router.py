from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_organizer,
    get_current_user,
    get_optional_user,
)
from app.modules.checklist.schemas import (
    ChecklistItemCreate,
    ChecklistItemUpdate,
    ChecklistItemResponse,
    ChecklistItemWithAssignments,
    ChecklistAssignmentResponse,
    ChecklistAssignmentCreate,
)
from app.modules.checklist.service import ChecklistService
from app.modules.users.models import User

router = APIRouter()


# Organizer endpoints
@router.post(
    "/events/{event_id}/items",
    response_model=ChecklistItemResponse,
    status_code=201,
)
def create_checklist_item(
    event_id: int,
    item_data: ChecklistItemCreate,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Create a checklist item for an event (organizer only)"""
    return ChecklistService.create_checklist_item(
        db, event_id, item_data.dict(), current_user.id
    )


@router.put("/items/{item_id}", response_model=ChecklistItemResponse)
def update_checklist_item(
    item_id: int,
    update_data: ChecklistItemUpdate,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Update a checklist item (organizer only)"""
    return ChecklistService.update_checklist_item(
        db, item_id, update_data.dict(exclude_unset=True), current_user.id
    )


@router.delete("/items/{item_id}")
def delete_checklist_item(
    item_id: int,
    current_user: User = Depends(get_current_organizer),
    db: Session = Depends(get_db),
):
    """Delete a checklist item (organizer only)"""
    ChecklistService.delete_checklist_item(db, item_id, current_user.id)
    return {"message": "Checklist item deleted successfully"}


# Participant endpoints
@router.post("/assign", response_model=ChecklistAssignmentResponse)
def assign_checklist_item(
    assignment_data: ChecklistAssignmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Assign a checklist item to the current user"""
    assignment = ChecklistService.assign_item_to_user(
        db, assignment_data.checklist_item_id, current_user.id
    )

    # Get user name for response
    user = db.query(User).filter(User.id == assignment.user_id).first()

    # Return custom response with user_name
    return {
        "id": assignment.id,
        "checklist_item_id": assignment.checklist_item_id,
        "user_id": assignment.user_id,
        "user_name": user.name if user else "Unknown",
        "assigned_at": assignment.assigned_at,
    }


@router.delete("/items/{item_id}/assign")
def remove_checklist_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove checklist item assignment from current user"""
    ChecklistService.remove_item_from_user(db, item_id, current_user.id)
    return {"message": "Item unassigned successfully"}


# Common endpoints
@router.get(
    "/events/{event_id}", response_model=List[ChecklistItemWithAssignments]
)
def get_event_checklist(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """Get full checklist for an event with assignment details including user names"""
    items = ChecklistService.get_event_checklist(db, event_id)
    result = []

    for item in items:
        # Get assignments with user information
        assignments_data = ChecklistService.get_item_assignments_with_users(
            db, item.id
        )

        # Convert to response objects
        assignments = [
            ChecklistAssignmentResponse(
                id=a["id"],
                checklist_item_id=a["checklist_item_id"],
                user_id=a["user_id"],
                user_name=a["user_name"],
                assigned_at=a["assigned_at"],
            )
            for a in assignments_data
        ]

        is_taken = len(assignments) > 0
        current_user_id = current_user.id if current_user else None
        taken_by_current_user = (
            any(a.user_id == current_user_id for a in assignments)
            if current_user_id is not None
            else False
        )

        result.append(
            ChecklistItemWithAssignments(
                **item.__dict__,
                assignments=assignments,
                is_taken=is_taken,
                taken_by_current_user=taken_by_current_user,
                taken_count=len(assignments),
            )
        )

    return result


@router.get(
    "/my-items/events/{event_id}", response_model=List[ChecklistItemResponse]
)
def get_my_checklist_items_for_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all checklist items assigned to current user for a specific event"""
    items = ChecklistService.get_user_items_for_event(
        db, current_user.id, event_id
    )
    return items
