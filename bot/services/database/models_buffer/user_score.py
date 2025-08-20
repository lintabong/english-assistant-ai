
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, BigInteger, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class UserScore(Base):
    __tablename__ = "user_scores"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    set_id = Column(Integer, ForeignKey("conversation_sets.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="scores")
    conversation_set = relationship("ConversationSet", back_populates="scores")
