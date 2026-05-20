from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.database import Base


class PIITokenMap(Base):

    __tablename__ = "pii_token_map"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(
        String(100),
        unique=True,
        nullable=False
    )

    real_value = Column(
        Text,
        nullable=False
    )

    pii_type = Column(String(50))

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
