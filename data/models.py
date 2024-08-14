from sqlalchemy import Column, Index, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # According to the "total count of messages" part in docs, I can
    # use this field as a total message count of a user, so I won't
    # need to call count() function in for read calls all the time,
    # which is considered performance de-booster.
    # @see EntryDAO.add() function.
    message_count = Column(Integer, default=0)

    # List of entries of this user.
    entries = relationship("Entry", back_populates="user")

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Owner user of this entry.
    user = relationship("User", back_populates="entries")

    # In case, full-text search is needed of PostgreSQL.
    # __table_args__ = (
    #     Index('ix_entries_subject_tsv', func.to_tsvector('english', subject), postgresql_using='gin'),
    #     Index('ix_entries_message_tsv', func.to_tsvector('english', message), postgresql_using='gin'),
    # )
