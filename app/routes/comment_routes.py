from app.services.comment_service import get_comments_by_ticket, create_comment
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.comment_schema import CommentCreate, CommentResponse
import requests

NOTIFICATION_URL = "http://localhost:8084/notifications/event"
TICKET_SERVICE_URL = "http://localhost:8082/tickets"

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("", response_model=CommentResponse)
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):

    if not comment.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    saved_comment = create_comment(db, comment)

    # 🔍 Fetch ticket to get student (creator)
    try:
        ticket_resp = requests.get(f"{TICKET_SERVICE_URL}/{comment.ticket_id}")
        ticket_resp.raise_for_status()
        ticket = ticket_resp.json()
        student_id = ticket["createdBy"]
    except Exception:
        return saved_comment   # ❌ Do not block comment flow

    # 🔔 Notify STUDENT
    try:
        requests.post(
            NOTIFICATION_URL,
            json={
                "event_type": "TICKET_COMMENT_ADDED",
                "ticket_id": comment.ticket_id,
                "actor_id": comment.user_id,
                "actor_role": "AGENT",
                "recipient_id": student_id
            }
        )
    except Exception:
        pass

    return saved_comment


@router.get("/{ticket_id}", response_model=list[CommentResponse])
def fetch_comments(ticket_id: int, db: Session = Depends(get_db)):
    return get_comments_by_ticket(db, ticket_id)
