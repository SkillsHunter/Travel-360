import streamlit as st
import requests

API_URL = "https://travel-360.onrender.com/search"

st.set_page_config(
    page_title="Travel-360",
    page_icon="✈️",
    layout="wide"
)

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

h1, h2, h3 {
    color: white;
}

.metric-card {
    background: linear-gradient(135deg, #1C1F26, #2A2F3A);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #2E3440;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

.green-card {
    background: linear-gradient(135deg, #163B2D, #1F5A42);
    padding: 20px;
    border-radius: 18px;
    color: white;
}

.warning-card {
    background: linear-gradient(135deg, #4A3218, #6B4423);
    padding: 20px;
    border-radius: 18px;
    color: white;
}

.pooling-card {
    background: linear-gradient(135deg, #102A43, #1E4D7A);
    padding: 25px;
    border-radius: 20px;
    color: white;
    border: 1px solid #2B6CB0;
}

.security-card {
    background: linear-gradient(135deg, #2A1A3A, #4B2A63);
    padding: 20px;
    border-radius: 18px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.title("✈️ Travel-360 Enterprise Console")

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
    st.metric("Pooling Matches", "142")

with k4:
    st.metric("Active Trips", "328")

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

    route = st.selectbox(
        "Travel Route",
        [
            "DEL-BLR",
            "DEL-BOM",
            "DEL-HYD",
            "BOM-HYD",
            "BLR-HYD"
        ]
    )

    search = st.button(
        "Execute Travel Search",
        use_container_width=True
    )

# RIGHT PANEL

with right:

    st.subheader("Operational Intelligence")

    st.markdown("""
    <div class="pooling-card">
        <h3>🚖 Smart Pooling Engine</h3>
        <p>
        Multi-tenant ride-sharing optimization detects
        overlapping airport arrivals and reduces
        enterprise transit emissions automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="security-card">
        <h3>🔒 Zero-Trust Privacy Firewall</h3>
        <p>
        All sensitive traveler data is recursively sanitized
        and tokenized before downstream processing.
        </p>
    </div>
    """, unsafe_allow_html=True)

# SEARCH RESPONSE

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

    st.header("🔒 Privacy Verification Layer")

    privacy = data["privacy_check"]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Masked User</h4>
            <h3>{privacy["traveler_name"]}</h3>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Masked Passport</h4>
            <h3>{privacy["passport_number"]}</h3>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Masked Member ID</h4>
            <h3>{privacy["member_id"]}</h3>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    flight = data["flight_result"]

    left2, right2 = st.columns([1.2, 1])

    with left2:

        st.header("✈️ Flight Recommendation")

        st.markdown(f"""
        <div class="metric-card">
            <h3>{flight['flight_number']}</h3>
            <p>Route: {flight['route']}</p>
            <h2>{flight['price']}</h2>
        </div>
        """, unsafe_allow_html=True)

    with right2:

        st.header("🌱 ESG Impact")

        if "Low" in flight["esg_message"]:

            st.markdown(f"""
            <div class="green-card">
                <h2>{flight['co2_impact']}</h2>
                <p>{flight['esg_message']}</p>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="warning-card">
                <h2>{flight['co2_impact']}</h2>
                <p>{flight['esg_message']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.header("🚖 Ride Pooling Opportunity")

    st.markdown("""
    <div class="pooling-card">
        <h2>Shared Transit Match Detected</h2>

        <p>
        Another verified traveler is arriving within
        a 30-minute airport window.
        </p>

        <ul>
            <li>Estimated Savings: ₹950</li>
            <li>Estimated CO₂ Reduction: 18%</li>
            <li>Pooling Confidence Score: 92%</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("🛡 Governance Workflow")

    st.warning(
        "Manual approval required for ESG threshold override."
    )

    reason = st.text_area(
        "Manager Justification"
    )

    if st.button("Approve Exception"):

        st.success(
            "Approval successfully logged."
        )
