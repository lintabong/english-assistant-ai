from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from bot.services.database import Base


class LLMLog(Base):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String(24), nullable=True)          # optional, kalau ada user terkait
    message = Column(Text, nullable=False)               # input user / pertanyaan
    system_instruction = Column(Text, nullable=True)     # instruksi system prompt
    response = Column(Text, nullable=False)              # jawaban LLM
    input_token = Column(Integer, default=0)             # jumlah token input
    output_token = Column(Integer, default=0)            # jumlah token output
    created_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
