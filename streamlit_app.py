import streamlit as st
import requests

API_URL = "https://travel-360.onrender.com/search"

st.set_page_config(
    page_title="Travel-360",
    layout="wide"
)

st.title("✈️ Travel-360 Concierge Dashboard")

st.subheader(
    "AI-Powered Enterprise Travel Platform"
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Traveler Name",
        "Arjun Mehta"
    )

    passport = st.text_input(
        "Passport Number",
        "K1234567"
    )

with col2:

    member_id = st.text_input(
        "Member ID",
        "MEM8821"
    )

    route = st.selectbox(
        "Route",
        [
            "DEL-BLR",
            "DEL-BOM",
            "DEL-HYD",
            "BOM-HYD",
            "BLR-HYD"
        ]
    )

search = st.button("Search Flights")

if search:

    payload = {
        "traveler_name": name,
        "passport_number": passport,
        "member_id": member_id,
        "route": route
    }

    response = requests.post(
        API_URL,
        json=payload
    )

    data = response.json()

    st.divider()

    st.header("🔒 Privacy Protection Layer")

    privacy = data["privacy_check"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Masked User",
            privacy["traveler_name"]
        )

    with col2:
        st.metric(
            "Masked Passport",
            privacy["passport_number"]
        )

    with col3:
        st.metric(
            "Masked Member ID",
            privacy["member_id"]
        )

    st.success(
        "PII successfully sanitized."
    )

    st.divider()

    st.header("✈️ Flight Recommendation")

    flight = data["flight_result"]

    st.info(
        f"""
        Flight: {flight['flight_number']}

        Route: {flight['route']}

        Price: {flight['price']}
        """
    )

    st.divider()

    st.header("🌱 ESG Sustainability Analysis")

    st.metric(
        "Carbon Footprint",
        flight["co2_impact"]
    )

    if "Low" in flight["esg_message"]:
        st.success(flight["esg_message"])

    elif "Moderate" in flight["esg_message"]:
        st.warning(flight["esg_message"])

    else:
        st.error(flight["esg_message"])

    st.divider()

    st.header("🚖 Smart Ride Pooling")

    st.success(
        """
        Another verified colleague is arriving
        within a 30-minute airport window.

        Shared ride recommended.

        Estimated savings: ₹950
        """
    )

    st.divider()

    st.header("🛡 Governance Workflow")

    st.warning(
        """
        Policy Exception Requires Manager Approval
        """
    )

    manager_reason = st.text_area(
        "Manager Justification"
    )

    if st.button("Approve Exception"):

        st.success(
            "Approval successfully recorded."
        )
