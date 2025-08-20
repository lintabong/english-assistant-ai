from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class UserConversation(Base):
    __tablename__ = "user_conversation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_set_id = Column(Integer, ForeignKey("conversation_sets.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="conversations")
    conversation_set = relationship("ConversationSet", back_populates="user_configs")

