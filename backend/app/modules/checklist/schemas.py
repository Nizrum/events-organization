from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChecklistItemBase(BaseModel):
    title: str
    type: str  # single or multiple


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItemUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None


class ChecklistItemResponse(ChecklistItemBase):
    id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChecklistAssignmentResponse(BaseModel):
    id: int
    checklist_item_id: int
    user_id: int
    user_name: str  # Добавлено поле с именем пользователя
    assigned_at: datetime

    class Config:
        from_attributes = True


class ChecklistItemWithAssignments(ChecklistItemResponse):
    assignments: List[ChecklistAssignmentResponse] = []
    is_taken: bool = False
    taken_by_current_user: bool = False
    taken_count: int = 0


class ChecklistAssignmentCreate(BaseModel):
    checklist_item_id: int
