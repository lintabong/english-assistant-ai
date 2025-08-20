from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, BigInteger, Text
from sqlalchemy.orm import relationship
from bot.services.database import Base

class UserConversationLog(Base):
    __tablename__ = "user_conversation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("conversation_items.id", ondelete="CASCADE"), nullable=False)
    answer = Column(Text)
    score = Column(Integer)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    answered_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="logs")
    item = relationship("ConversationItem", back_populates="logs")