
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from datetime import datetime
from bot.services.database import Base

class Package(Base):
    __tablename__ = 'packages'
    id = Column(String(24), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    quota_prompt = Column(Integer, default=100, nullable=False)
    quota_input = Column(Integer, default=1000, nullable=False)
    quota_output = Column(Integer, default=500, nullable=False)
    calendar = Column(Boolean, default=False)
    advanced_reports = Column(Boolean, default=False)
    api_access = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
