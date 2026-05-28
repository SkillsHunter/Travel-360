from fastapi import APIRouter, Depends
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


@router.post("/search")
async def search_travel(
    payload: dict,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # PRIVACY SANITIZATION
    # -----------------------------

    deid = DeIdentificationService(db)

    sanitized_payload = deid.sanitize(payload)

    # -----------------------------
    # FLIGHT LOOKUP
    # -----------------------------

    route = payload.get("route")

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

        traveler_name=payload.get(
            "traveler_name"
        ),

        airport_code=airport_code,

        travel_date=payload.get("travel_date"),

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

            "total_matches": len(
                pooling_matches
            ),

            "airport_code": airport_code,

            "travel_date": payload.get(
                "travel_date"
            )
        }
    }
