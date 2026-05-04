from pydantic import BaseModel
from typing import Optional


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20


class MessageResponse(BaseModel):
    message: str
    details: Optional[str] = None
