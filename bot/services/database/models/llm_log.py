from sqlalchemy import (
    Column, Integer, String, Text, DateTime, func
)
from bot.services.database import Base

class LLMLog(Base):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(24), nullable=True)
    message = Column(Text, nullable=False)
    system_instruction = Column(Text)
    response = Column(Text, nullable=False)
    input_token = Column(Integer, default=0)
    output_token = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
