
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from datetime import datetime
from bot.services.database import Base

class Cashflow(Base):
    __tablename__ = 'cashflows'
    id = Column(String(24), primary_key=True)
    user_id = Column(String(24), ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
