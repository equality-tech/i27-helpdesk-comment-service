import pytest
from pydantic import ValidationError

from app.models.comment_schema import CommentCreate, CommentResponse


def test_comment_create_accepts_complete_payload():
    comment = CommentCreate(ticket_id=10, commented_by=3, commented_by_role="STUDENT", comment="Need help")
    assert comment.ticket_id == 10


def test_comment_create_keeps_author_role():
    comment = CommentCreate(ticket_id=10, commented_by=3, commented_by_role="AGENT", comment="Looking into it")
    assert comment.commented_by_role == "AGENT"


def test_comment_create_requires_comment_text():
    with pytest.raises(ValidationError):
        CommentCreate(ticket_id=10, commented_by=3, commented_by_role="STUDENT")


def test_comment_create_requires_author_role():
    with pytest.raises(ValidationError):
        CommentCreate(ticket_id=10, commented_by=3, comment="Need help")


def test_comment_response_allows_missing_creation_time():
    response = CommentResponse(id=1, ticket_id=10, commented_by=3, commented_by_role="STUDENT", comment="Need help", created_at=None)
    assert response.created_at is None
