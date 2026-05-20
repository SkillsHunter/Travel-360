from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    JSON,
    TIMESTAMP
)

from sqlalchemy.sql import func

from app.db.database import Base


class SupervisorDecisionLog(Base):

    __tablename__ = "supervisor_decision_log"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String(100))

    policy_result = Column(JSON)

    ranking_score = Column(Float)

    esg_score = Column(Float)

    approved = Column(Boolean)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
