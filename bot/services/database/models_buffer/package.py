
from sqlalchemy import Column, String, Integer, Text, DateTime, func
from sqlalchemy.orm import relationship

from bot.services.database import Base

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    quota_prompt = Column(Integer, default=3, nullable=False)
    quota_input = Column(Integer, default=4, nullable=False)
    quota_output = Column(Integer, default=4, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("UserPackage", back_populates="package")
