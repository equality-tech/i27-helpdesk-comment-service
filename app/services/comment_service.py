from sqlalchemy.orm import Session
import requests

from app.models.comment import Comment
from app.models.comment_schema import CommentCreate
import os
# 🔔 Notification Service
NOTIFICATION_URL = os.environ["NOTIFICATION_URL"]
TICKET_SERVICE_URL = os.environ["TICKET_SERVICE_URL"]

# =====================================================
# ✍️ Create comment
# =====================================================
def create_comment(db: Session, comment_data: CommentCreate):

    comment = Comment(
        ticket_id=comment_data.ticket_id,
        commented_by=comment_data.commented_by,
        commented_by_role=comment_data.commented_by_role,
        comment=comment_data.comment
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    # =================================================
    # 🔔 Emit COMMENT event (NO recipient logic here)
    # =================================================
    try:
        payload = {
            "event_type": "TICKET_COMMENT_ADDED",   # ✅ FIXED
            "ticket_id": comment_data.ticket_id,
            "actor_id": comment_data.commented_by,
            "actor_role": comment_data.commented_by_role
        }

        requests.post(
            NOTIFICATION_URL,
            json=payload,
            timeout=3
        )

    except Exception as e:
        # 🔥 Never break comment flow
        print("⚠️ Failed to emit comment event:", e)

    return comment


# =====================================================
# 📄 Retrieve comments for a ticket
# =====================================================
def get_comments_by_ticket(db: Session, ticket_id: int):
    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
