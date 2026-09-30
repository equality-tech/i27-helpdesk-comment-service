
from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, String
from sqlalchemy.sql import func
from app.db.database import Base



class Comment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(BigInteger, nullable=False)
    commented_by = Column(BigInteger, nullable=False)  # user_id from auth-service
    commented_by_role = Column(String(20), nullable=False)  # role of the commenter

    comment = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
