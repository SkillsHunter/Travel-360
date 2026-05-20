from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.database import Base


class PIIAuditLog(Base):

    __tablename__ = "pii_audit_log"

    id = Column(Integer, primary_key=True, index=True)

    field_name = Column(String(100))

    masked_value = Column(Text)

    timestamp = Column(
        TIMESTAMP,
        server_default=func.now()
    )
