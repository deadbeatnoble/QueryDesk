from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    text = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)