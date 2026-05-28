from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class TravelRequest(Base):

    __tablename__ = "travel_requests"

    request_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(String)

    traveler_name = Column(String)

    airport_code = Column(String)

    route = Column(String)

    travel_date = Column(String)

    request_time = Column(
        DateTime,
        default=datetime.utcnow
    )
