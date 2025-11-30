import streamlit as st
import base64
import os

# -----------------------------
# LOGIN CHECK
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

st.title("🌍 Choose Your Country")

st.write("Select a country to explore its cities:")

# -----------------------------
# LOAD IMAGES 
# -----------------------------
def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

  
country_images_base64 = {
    "India": load_image_base64("images/india.png"),    
    "United Kingdom": load_image_base64("images/uk.png")
}

# -----------------------------
# AVAILABLE COUNTRIES
# -----------------------------
countries = list(country_images_base64.keys())

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.country-card {
    background: rgba(255,255,255,0.15);
    padding: 15px;
    border-radius: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}
.country-card:hover {
    transform: scale(1.05);
}
.country-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 14px;
}
.country-name {
    font-size: 22px;
    font-weight: 700;
    padding-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DISPLAY COUNTRY CARDS
# -----------------------------
for i in range(0, len(countries), 2):
    
    col1, col2 = st.columns(2)

    # COUNTRY 1
    if i < len(countries):
        country_name = countries[i]
        with col1:
            st.markdown(
                f"""
                <div class="country-card">
                    <img src="data:image/png;base64,{country_images_base64[country_name]}" class="country-img" />
                    <div class="country-name">{country_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Select {country_name}", key=f"{country_name}_btn"):
                st.session_state["selected_country"] = country_name
                st.switch_page("pages/3_City_Selection.py")

    # COUNTRY 2
    if i + 1 < len(countries):
        country_name = countries[i + 1]
        with col2:
            st.markdown(
                f"""
                <div class="country-card">
                    <img src="data:image/png;base64,{country_images_base64[country_name]}" class="country-img" />
                    <div class="country-name">{country_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Select {country_name}", key=f"{country_name}_btn2"):
                st.session_state["selected_country"] = country_name
                st.switch_page("pages/3_City_Selection.py")