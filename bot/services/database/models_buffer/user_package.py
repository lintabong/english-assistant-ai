
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from bot.services.database import Base

class UserPackage(Base):
    __tablename__ = "user_package"

    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    quota_prompt = Column(Integer, nullable=False)
    quota_input = Column(Integer, nullable=False)
    quota_output = Column(Integer, nullable=False)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="package")
    package = relationship("Package", back_populates="users")
