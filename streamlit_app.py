import streamlit as st
import requests
import pandas as pd

API_URL = "https://travel-360.onrender.com/search"

# LOAD FLIGHTS DATA
FLIGHTS_DF = pd.read_csv("data/flights.csv")

# PAGE CONFIG
st.set_page_config(
    page_title="Travel-360",
    page_icon="✈️",
    layout="wide"
)

# SESSION STATE
if "approval_status" not in st.session_state:
    st.session_state.approval_status = False

# CUSTOM CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4 {
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #1C1F26;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #2E3440;
}

html, body, [class*="css"] {
    background-color: #0E1117;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.title("✈️ Travel-360 Enterprise Console")

st.success("NEW VERSION DEPLOYED")

st.caption(
    "Autonomous Enterprise Logistics & Compliance Platform"
)

st.divider()

# KPI ROW
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Compliance Rate", "96%")

with k2:
    st.metric("CO₂ Saved", "18.4 Tons")

with k3:
    st.metric("Pooling Opportunities", "142")

with k4:
    st.metric("Active Trips", "328")

st.divider()

# FLIGHT INVENTORY
st.subheader("📊 Live Flight Inventory")

inventory1, inventory2, inventory3 = st.columns(3)

with inventory1:
    st.metric(
        "Available Flights",
        len(FLIGHTS_DF)
    )

with inventory2:

    avg_co2 = int(
        FLIGHTS_DF["co2_kg"].mean()
    )

    st.metric(
        "Average CO₂",
        f"{avg_co2} kg"
    )

with inventory3:

    avg_price = int(
        FLIGHTS_DF["price_inr"].mean()
    )

    st.metric(
        "Average Fare",
        f"₹{avg_price}"
    )

display_df = FLIGHTS_DF.rename(
    columns={
        "flight_number": "Flight",
        "airline": "Airline",
        "route": "Route",
        "departure_time": "Departure",
        "arrival_time": "Arrival",
        "duration_mins": "Duration (mins)",
        "price_inr": "Price (₹)",
        "co2_kg": "CO₂ Impact (kg)",
        "seats_available": "Seats",
        "cabin_class": "Cabin",
        "esg_rating": "ESG Rating",
        "airport_code": "Airport"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    height=350
)

st.divider()

# MAIN LAYOUT
left, right = st.columns([1, 1.4])

# LEFT PANEL
with left:

    st.subheader("Traveler Request")

    name = st.text_input(
        "Traveler Name",
        "Arjun Mehta"
    )

    passport = st.text_input(
        "Passport Number",
        "K1234567"
    )

    member_id = st.text_input(
        "Member ID",
        "MEM8821"
    )

    travel_date = st.date_input(
        "Travel Date"
    )

    company_id = st.selectbox(
        "Company",
        [
            "COMPANY_A",
            "COMPANY_B",
            "COMPANY_C",
            "COMPANY_D"
        ]
    )

    available_routes = FLIGHTS_DF["route"].unique()

    route = st.selectbox(
        "Travel Route",
        available_routes
    )

    search = st.button(
        "Execute Travel Search",
        use_container_width=True
    )

# RIGHT PANEL
with right:

    st.subheader("Operational Intelligence")

    st.info(
        """
        🚖 Smart Pooling Engine
        
        Multi-tenant ride-sharing optimization detects
        overlapping airport arrivals and reduces
        enterprise transit emissions automatically.
        """
    )

    st.warning(
        """
        🔒 Zero-Trust Privacy Firewall
        
        All sensitive traveler data is recursively sanitized
        and tokenized before downstream processing.
        """
    )

# SEARCH RESPONSE
if search:

    payload = {
        "traveler_name": name,
        "passport_number": passport,
        "member_id": member_id,
        "company_id": company_id,
        "route": route,
        "travel_date": str(travel_date)
    }

    try:

        response = requests.post(
            API_URL,
            json=payload
        )

        if response.status_code != 200:

            st.error(
                f"Backend Error: {response.status_code}"
            )

            st.stop()

        data = response.json()

        st.divider()

        # PRIVACY LAYER
        st.header("🔒 Privacy Verification Layer")

        privacy = data.get("privacy_check", {})

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Masked User",
                privacy.get("traveler_name", "N/A")
            )

        with c2:
            st.metric(
                "Masked Passport",
                privacy.get("passport_number", "N/A")
            )

        with c3:
            st.metric(
                "Masked Member ID",
                privacy.get("member_id", "N/A")
            )

        st.divider()

        # FLIGHT RESULT
        flight = data.get("flight_result", {})

        left2, right2 = st.columns([1.2, 1])

        with left2:

            st.header("✈️ Flight Recommendation")

            with st.container(border=True):

                st.subheader(
                    f"{flight['airline']} • {flight['flight_number']}"
                )

                st.write(
                    f"**Route:** {flight['route']}"
                )

                st.write(
                    f"**Date:** {flight['travel_date']}"
                )

                st.write(
                    f"**Departure:** {flight['departure_time']}"
                )

                st.write(
                    f"**Arrival:** {flight['arrival_time']}"
                )

                st.write(
                    f"**Cabin:** {flight['cabin_class']}"
                )

                st.write(
                    f"**ESG Rating:** {flight['esg_rating']}"
                )

                st.success(
                    f"Fare: {flight['price']}"
                )

        with right2:

            st.header("🌱 ESG Impact")
            st.metric(
                "ESG Rating",
                flight.get("esg_rating", "N/A")
            )

            if "Low" in flight["esg_message"]:

                st.success(
                    f"""
                    CO₂ Impact: {flight['co2_impact']}
                    
                    {flight['esg_message']}
                    """
                )

            else:

                st.warning(
                    f"""
                    CO₂ Impact: {flight['co2_impact']}
                    
                    {flight['esg_message']}
                    """
                )

        st.divider()

        # LIVE SQL POOLING
        st.header("🚖 Ride Pooling Opportunity")

        pooling = data.get("pooling", {})

        if pooling.get("match_found"):

            st.success(
                "🚖 Shared Transit Match Detected"
            )

            st.write(
                """
                Multi-tenant ride-sharing opportunity identified
                using real-time airport arrival matching.
                """
            )

            st.write(
                f"• Pooling Opportunities: {pooling.get('total_matches')}"
            )

            st.write(
                f"• Airport: {pooling.get('airport_code')}"
            )

            st.write(
                f"• Travel Date: {pooling.get('travel_date')}"
            )

            st.write(
                "• Estimated Savings: ₹950"
            )

            st.write(
                "• Estimated CO₂ Reduction: 18%"
            )

            st.write(
                "• Pooling Confidence Score: 92%"
            )

        else:

            st.info(
                "No live pooling opportunities detected."
            )

        st.divider()

        # GOVERNANCE
        
        st.header("🛡 Governance Workflow")
        
        if flight.get("flight_number") == "AI550":
        
            st.error(
                """
                This itinerary exceeds the corporate ESG threshold
                and normally requires mitigation before booking.
                """
            )
        
            bypass = st.checkbox(
                "Authorize departmental carbon credit allocation for this trip."
            )
        
            if bypass:
        
                st.success(
                    """
                    Carbon mitigation authorized.
        
                    Restriction cleared dynamically.
        
                    Proceeding to checkout.
                    """
                )
        
                st.balloons()
        
        else:
        
            st.success(
                """
                Flight complies with enterprise sustainability policy.
        
                No governance intervention required.
                """
            )

    except Exception as e:

        st.error(
            "Backend connection failed. Please check Render deployment."
        )

        st.exception(e)
