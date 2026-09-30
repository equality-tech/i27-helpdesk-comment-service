from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    ticket_id: int
    commented_by: int
    commented_by_role: str   # ✅ REQUIRED NOW
    comment: str

class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    commented_by: int
    commented_by_role: str
    comment: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True