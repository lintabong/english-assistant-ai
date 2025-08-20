
import enum
from sqlalchemy import (
    Column, String, BigInteger, Enum, Boolean, DateTime, func
)
from sqlalchemy.orm import relationship
from bot.services.database import Base

class UserType(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(String(24), primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100))
    email = Column(String(150))
    password = Column(String(255))
    type = Column(Enum(UserType), default=UserType.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    package = relationship("UserPackage", back_populates="user", uselist=False)
    conversations = relationship("UserConversation", back_populates="user")
    logs = relationship("UserConversationLog", back_populates="user")
    scores = relationship("UserScore", back_populates="user")
