from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.core.database import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # single or multiple
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChecklistAssignment(Base):
    __tablename__ = "checklist_assignments"

    id = Column(Integer, primary_key=True, index=True)
    checklist_item_id = Column(
        Integer,
        ForeignKey("checklist_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "checklist_item_id", "user_id", name="unique_item_user"
        ),
    )
