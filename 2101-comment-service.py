from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.comment_schema import CommentCreate


def create_comment(db: Session, comment_data: CommentCreate):
    comment = Comment(
        ticket_id=comment_data.ticket_id,
        commented_by=comment_data.commented_by,
        commented_by_role=comment_data.commented_by_role,  # ✅ NEW
        comment=comment_data.comment
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# Retrieve comments for a specific ticket
def get_comments_by_ticket(db: Session, ticket_id: int):
    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.created_at.asc())
        .all()
    )