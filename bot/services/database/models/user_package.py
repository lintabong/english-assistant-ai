
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from bot.services.database import Base

class UserPackage(Base):
    __tablename__ = 'user_packages'
    id = Column(String(24), primary_key=True)
    user_id = Column(String(24), ForeignKey('users.id'), nullable=False)
    package_id = Column(String(24), ForeignKey('packages.id'), nullable=False)
    quota_prompt = Column(Integer, nullable=False)
    quota_input = Column(Integer, nullable=False)
    quota_output = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
