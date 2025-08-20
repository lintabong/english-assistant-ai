
from sqlalchemy import Column, String, BigInteger, Enum, Boolean, DateTime
from datetime import datetime
from bot.services.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String(24), primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100))
    email = Column(String(150))
    password = Column(String(255), nullable=False)
    type = Column(Enum('superadmin', 'admin', 'user', 'employee', name='user_type'), default='user')
    is_active = Column(Boolean, default=True)
    used_cashflow_id = Column(String(24))
    created_at = Column(DateTime, default=datetime.utcnow)
