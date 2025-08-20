from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship

from bot.services.database import Base


class ConversationSet(Base):
    __tablename__ = "conversation_sets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100))
    speaker = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    items = relationship("ConversationItem", back_populates="set", cascade="all, delete-orphan")
    user_configs = relationship("UserConversation", back_populates="conversation_set")
    scores = relationship("UserScore", back_populates="conversation_set")
