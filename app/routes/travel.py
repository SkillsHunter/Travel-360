import os
import secrets
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.models.travel_request import TravelRequest
from app.services.pooling_service import find_pooling_matches

from app.db.database import get_db

from app.services.deid_service import DeIdentificationService

from app.services.esg_service import (
    get_flight_data,
    green_message
)

router = APIRouter()


# Optional shared key. When TRAVEL360_API_KEY is set on the server,
# every /search call must send it in the X-API-Key header.
API_KEY = os.getenv("TRAVEL360_API_KEY")


def require_api_key(x_api_key: Optional[str] = Header(default=None)):

    if API_KEY and not (
        x_api_key and secrets.compare_digest(x_api_key, API_KEY)
    ):
        raise HTTPException(status_code=401, detail="Invalid API key")


class SearchRequest(BaseModel):

    traveler_name: Optional[str] = Field(default=None, max_length=100)

    passport_number: Optional[str] = Field(default=None, max_length=20)

    member_id: Optional[str] = Field(default=None, max_length=40)

    company_id: str = Field(default="COMPANY_A", max_length=40)

    # Format: three-letter origin and destination codes, e.g. DEL-BLR
    route: str = Field(pattern=r"^[A-Z]{3}-[A-Z]{3}$")

    travel_date: date

    @field_validator("route", mode="before")
    @classmethod
    def normalise_route(cls, value):

        if isinstance(value, str):
            return value.strip().upper()

        return value


@router.post("/search", dependencies=[Depends(require_api_key)])
async def search_travel(
    request: SearchRequest,
    db: Session = Depends(get_db)
):

    payload = request.model_dump(mode="json", exclude_none=True)

    # -----------------------------
    # PRIVACY SANITIZATION
    # -----------------------------

    deid = DeIdentificationService(db)

    sanitized_payload = deid.sanitize(payload)

    # -----------------------------
    # FLIGHT LOOKUP
    # -----------------------------

    route = payload["route"]

    flight = get_flight_data(route)

    if not flight:

        return {
            "error": "No flight found"
        }

    # -----------------------------
    # STORE TRAVEL REQUEST
    # -----------------------------

    airport_code = route.split("-")[-1]

    new_request = TravelRequest(
        company_id=payload.get(
            "company_id",
            "COMPANY_A"
        ),

        # Store the token, never the raw name
        traveler_name=sanitized_payload.get(
            "traveler_name"
        ),

        airport_code=airport_code,

        travel_date=payload.get(
            "travel_date"
        ),

        route=route
    )

    db.add(new_request)

    db.commit()

    # -----------------------------
    # EXECUTE POOLING QUERY
    # -----------------------------

    pooling_matches = find_pooling_matches(db)

    pooling_detected = (
        len(pooling_matches) > 0
    )
    
    # # COUNT UNIQUE TRAVELERS
    # unique_travelers = set()
    
    # for row in pooling_matches:
    
    #     unique_travelers.add(row.ID_A)
    #     unique_travelers.add(row.ID_B)
    
    # total_pooling_travelers = len(
    #     unique_travelers
    # )

    # COUNT UNIQUE TRAVELERS

    unique_travelers = set()
    
    for row in pooling_matches:
    
        unique_travelers.add(row[0])  # ID_A
        unique_travelers.add(row[3])  # ID_B
    
    total_pooling_travelers = len(
        unique_travelers
    )

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------

    return {

        "privacy_check": sanitized_payload,

        "flight_result": {

            "flight_number": flight["flight_number"],

            "airline": flight["airline"],

            "route": flight["route"],

            "departure_time": flight["departure_time"],

            "arrival_time": flight["arrival_time"],

            "duration_mins": flight["duration_mins"],

            "price": f"₹{flight['price_inr']}",

            "co2_impact": f"{flight['co2_kg']} kg",

            "esg_rating": flight["esg_rating"],

            "cabin_class": flight["cabin_class"],

            "travel_date": payload.get(
                "travel_date"
            ),

            "esg_message": green_message(
                flight["co2_kg"]
            )
        },

        "pooling": {

            "match_found": pooling_detected,

            "total_matches": total_pooling_travelers,

            "airport_code": airport_code,

            "travel_date": payload.get(
                "travel_date"
            )
        }
    }
