
from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, func
from bot.services.database import Base

class IntentLog(Base):
    __tablename__ = "intent_logs"
    id = Column(Integer, primary_key=True)
    input_message = Column(Text, nullable=False)
    intent_result = Column(String(100), nullable=False)
    intent_score = Column(Numeric(5, 4))
    created_at = Column(TIMESTAMP, server_default=func.now())
