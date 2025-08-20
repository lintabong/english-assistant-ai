from sqlalchemy import (
    Column, Integer, String, BigInteger, Boolean, DateTime, Enum,
    ForeignKey, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(24), primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100))
    email = Column(String(150))
    password = Column(String(255))
    type = Column(Enum("superadmin", "admin", "user", name="user_type"), default="user")
    is_active = Column(Boolean, default=True)
    conversation_set_id = Column(Integer, ForeignKey("conversation_sets.id", ondelete="SET DEFAULT"), default=1)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # relasi
    conversation_set = relationship("ConversationSet", back_populates="users")
    logs = relationship("UserConversationLog", back_populates="user")
