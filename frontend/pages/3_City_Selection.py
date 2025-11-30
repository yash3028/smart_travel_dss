import streamlit as st
import os

# -------------------------
# LOGIN CHECK
# -------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

# -------------------------
# COUNTRY CHECK
# -------------------------
if "selected_country" not in st.session_state:
    st.error("Please select a country first.")
    st.stop()

country = st.session_state["selected_country"]

st.title(f"🏙️ Cities in {country}")
st.write("Choose a city to explore more details.")

# -------------------------
# CITY IMAGES
# -------------------------
city_images = {
    "India": {
        "Mumbai": "images/mumbai.png",
        "Hyderabad": "images/hyd.png"
    },
    "United Kingdom": {
        "London": "images/london.png",
        "Edinburgh": "images/edinburgh.png"
    }
}

cities = list(city_images[country].keys())

# -------------------------
# CARD STYLING
# -------------------------
st.markdown("""
<style>
.country-card {
    background: rgba(255,255,255,0.15);
    padding: 16px;
    border-radius: 18px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}
.city-card:hover {
    transform: scale(1.05);
}
.city-name {
    font-size: 22px;
    font-weight: 700;
    padding-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# DISPLAY CITY CARDS (using st.image)
# -------------------------
for i in range(0, len(cities), 2):

    col1, col2 = st.columns(2)

    # CITY 1
    if i < len(cities):
        city = cities[i]
        with col1:
            st.markdown("<div class='city-card'>", unsafe_allow_html=True)
            st.image(city_images[country][city], use_container_width=True)
            st.markdown(f"<div class='city-name'>{city}</div>", unsafe_allow_html=True)
            if st.button(f"View {city}", key=f"{city}_btn"):
                st.session_state["selected_city"] = city
                st.switch_page("pages/4_Trip_Planner.py")
            st.markdown("</div>", unsafe_allow_html=True)

    # CITY 2
    if i + 1 < len(cities):
        city = cities[i + 1]
        with col2:
            st.markdown("<div class='city-card'>", unsafe_allow_html=True)
            st.image(city_images[country][city], use_container_width=True)
            st.markdown(f"<div class='city-name'>{city}</div>", unsafe_allow_html=True)
            if st.button(f"View {city}", key=f"{city}_btn2"):
                st.session_state["selected_city"] = city
                st.switch_page("pages/4_Trip_Planner.py")
            st.markdown("</div>", unsafe_allow_html=True)