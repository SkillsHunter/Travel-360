import streamlit as st
import requests

st.title("Travel-360")

name = st.text_input("Traveler Name")

passport = st.text_input("Passport Number")

member_id = st.text_input("Member ID")

route = st.text_input(
    "Route (Example: DEL-BLR)"
)

if st.button("Search Flight"):

    payload = {
        "traveler_name": name,
        "passport_number": passport,
        "member_id": member_id,
        "route": route
    }

    response = requests.post(
        "http://localhost:8000/search",
        json=payload
    )

    st.json(response.json())
