
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from bot.services.database import Base

class LLMLog(Base):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    intent = Column(String(20), nullable=True)
    system_instruction = Column(Text, nullable=True)
    response = Column(Text, nullable=False)
    input_token = Column(Integer, default=0)
    output_token = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
