from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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

    deid = DeIdentificationService(db)

    sanitized_payload = deid.sanitize(payload)

    route = payload.get("route")

    flight = get_flight_data(route)

    if not flight:
        return {
            "error": "No flight found"
        }

    return {
        "privacy_check": sanitized_payload,

        "flight_result": {
            "flight_number": flight["flight_number"],
            "route": flight["route"],
            "price": f"₹{flight['price_inr']}",
            "co2_impact": f"{flight['co2_kg']} kg",
            "esg_message": green_message(
                flight["co2_kg"]
            )
        }
    }
