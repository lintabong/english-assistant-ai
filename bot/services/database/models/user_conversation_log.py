from sqlalchemy import (
    Column, Integer, String, Text, BigInteger, DateTime, 
    ForeignKey, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class UserConversationLog(Base):
    __tablename__ = "user_conversation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("conversation_items.id", ondelete="CASCADE"), nullable=False)
    answer = Column(Text)
    sentence_score = Column(Integer, default=0)
    context_score = Column(Integer, default=0)
    sent_at = Column(DateTime, server_default=func.now())
    answered_at = Column(DateTime)

    # relasi
    user = relationship("User", back_populates="logs")
    item = relationship("ConversationItem", back_populates="logs")
