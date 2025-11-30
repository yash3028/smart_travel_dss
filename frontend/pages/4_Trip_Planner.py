import streamlit as st
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

# ------------------------------------------------
# PAGE TITLE
# ------------------------------------------------
st.title(f"🧳 Plan Your Trip to {city}")
st.write("Fill in your preferences to generate your personalized itinerary.")

# ------------------------------------------------
# PREMIUM UI STYLING
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
    
    days = st.slider("How many days are you planning to stay?", min_value=1, max_value=14, value=3)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# 2. BUDGET LEVEL
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    
    budget = st.selectbox(
        "What is your budget level?",
        ["Low Budget", "Medium Budget", "Luxury"]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# 3. INTERESTS
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)

    st.write("What are your interests?")
    interests = st.multiselect(
        "Select all that apply:",
        ["Nature", "Food", "Shopping", "Adventure", "Culture", "Relaxation"]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# 4. TRAVEL TYPE
# ------------------------------------------------
with st.container():
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)

    travel_type = st.radio(
        "Who are you travelling with?",
        ["Solo", "Friends", "Couple", "Family"],
        horizontal=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# BACKGROUND
# -----------------------------
def add_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
         [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
         [data-testid="stAppViewContainer"] .block-container {{
            background: rgba(255,255,255,0.7);
            padding: 20px;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg("images/genbg.png")

# ------------------------------------------------
# 5. GENERATE BUTTON
# ------------------------------------------------
generate = st.button("Generate My Itinerary", use_container_width=True)

# ------------------------------------------------
# ON CLICK → STORE DATA + SWITCH PAGE
# ------------------------------------------------
if generate:
    st.session_state["trip_days"] = days
    st.session_state["trip_budget"] = budget
    st.session_state["trip_interests"] = interests
    st.session_state["trip_travel_type"] = travel_type

    st.success("Building your custom itinerary…")
    st.switch_page("pages/5_Itinerary.py")