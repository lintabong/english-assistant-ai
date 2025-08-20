from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from bot.services.database import Base

class UserPackage(Base):
    __tablename__ = "user_package"

    # one-to-one ke users (PK = user_id)
    user_id = Column(String(24), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)

    quota_prompt = Column(Integer, nullable=False)
    quota_input  = Column(Integer, nullable=False)
    quota_output = Column(Integer, nullable=False)

    start_date = Column(DateTime, server_default=func.now(), nullable=False)
    end_date   = Column(DateTime, nullable=True)
