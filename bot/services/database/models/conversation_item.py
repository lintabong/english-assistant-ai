from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class ConversationItem(Base):
    __tablename__ = "conversation_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    set_id = Column(Integer, ForeignKey("conversation_sets.id", ondelete="CASCADE"), nullable=False)
    path = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # relasi
    set = relationship("ConversationSet", back_populates="items")
    logs = relationship("UserConversationLog", back_populates="item")
