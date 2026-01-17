import streamlit as st
import requests
import base64

# ------------------------------------------------
# LOGIN + CITY CHECK
# ------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

if "selected_city" not in st.session_state or "selected_country" not in st.session_state:
    st.error("Please select a city first.")
    st.stop()

country = st.session_state["selected_country"]
city = st.session_state["selected_city"]
headers = {
    "Authorization": f"Bearer {st.session_state['jwt']}"
}

# ------------------------------------------------
# PAGE TITLE
# ------------------------------------------------
st.title(f"🧳 Plan Your Trip to {city}")
st.write("Fill in your preferences to generate your personalized itinerary.")

# ------------------------------------------------
# STYLING
# ------------------------------------------------
st.markdown("""
<style>
.info-box {
    background: rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 1. NUMBER OF DAYS
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    days = st.slider(
        "How many days are you planning to stay?",
        min_value=1,
        max_value=14,
        value=3
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# 2. INTERESTS
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    interests = st.multiselect(
        "What are your interests?",
        ["Culture", "Nature", "Shopping", "Nightlife"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# 3. TRAVEL TYPE
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    travel_type = st.radio(
        "Who are you travelling with?",
        ["Solo", "Couple", "Family"],
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# BACKGROUND IMAGE
# ------------------------------------------------
def add_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("images/genbg.png")

# ------------------------------------------------
# GENERATE BUTTON
# ------------------------------------------------
generate = st.button("Generate My Itinerary", width="stretch")

# ------------------------------------------------
# ON CLICK → CALL ML VIA NODE BACKEND
# ------------------------------------------------
if generate:
    if not interests:
        st.error("Please select at least one interest.")
        st.stop()

    with st.spinner("Generating your personalized travel plan..."):
        try:
            # -----------------------------
            # Prepare payloads
            # -----------------------------
            budget_payload = {
                "city": city,
                "days": days,
                "travel_type": travel_type.lower(),
                "interest": interests[0].lower()
            }

            duration_payload = {
                "city": city,
                "interest": interests[0].lower(),
                "attractions": 15  # fixed / estimated value
            }

            # -----------------------------
            # Call Node Backend
            # -----------------------------
            budget_res = requests.post(
                "http://localhost:3001/api/auth/budget",
                json=budget_payload,
                headers=headers
            )

            duration_res = requests.post(
                "http://localhost:3001/api/auth/duration",
                json=duration_payload,
                headers=headers
            )

            st.write("Budget status:", budget_res.status_code)
            st.write("Budget response:", budget_res.text)

            st.write("Duration status:", duration_res.status_code)
            st.write("Duration response:", duration_res.text)

            if budget_res.status_code != 200 or duration_res.status_code != 200:
                st.error("Failed to generate trip.")
                st.stop()
            budget_data = budget_res.json()
            duration_data = duration_res.json()

            # -----------------------------
            # Save to session
            # -----------------------------
            st.session_state["trip_days"] = days
            st.session_state["trip_budget"] = budget_data["predicted_budget"]
            st.session_state["trip_interests"] = interests
            st.session_state["trip_travel_type"] = travel_type
            st.session_state["trip_duration"] = duration_data["predicted_duration"]

            
            st.switch_page("pages/5_Itinerary.py")

        except Exception as e:
            st.error("Backend or ML service not reachable.")
