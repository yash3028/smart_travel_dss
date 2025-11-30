import streamlit as st
from io import BytesIO
from fpdf import FPDF
import random
import base64


# ---------------------------------------------------
# CHECK REQUIRED SESSION DATA
# ---------------------------------------------------
required_keys = [
    "logged_in", "selected_country", "selected_city",
    "trip_days", "trip_budget", "trip_interests", "trip_travel_type"
]

for key in required_keys:
    if key not in st.session_state:
        st.error(f"Missing session key: {key}. Please complete previous steps.")
        st.stop()

if not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

# ---------------------------------------------------
# EXTRACT USER SELECTIONS
# ---------------------------------------------------
country = st.session_state["selected_country"]
city = st.session_state["selected_city"]
days = st.session_state["trip_days"]
budget = st.session_state["trip_budget"]
interests = st.session_state["trip_interests"]
travel_type = st.session_state["trip_travel_type"]

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title("Your Personalized Travel Itinerary")
st.subheader(f"{city}, {country}")
st.write(f"Trip Duration: **{days} days**")
st.write(f"Budget: **₹{budget}**")
st.write(f"Interests: **{', '.join(interests)}**")
st.write(f"Travel Type: **{travel_type}**")
st.markdown("---")

# ---------------------------------------------------
# FUNCTION TO GENERATE PDF (ASCII ONLY -> NO ERRORS)
# ---------------------------------------------------
def create_pdf(city, country, days, budget, interests, travel_type, itinerary_plan):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "Travel Itinerary", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Destination: {city}, {country}", ln=True)
    pdf.cell(0, 8, f"Trip Duration: {days} days", ln=True)
    pdf.cell(0, 8, f"Budget: Rs {budget}", ln=True)
    pdf.cell(0, 8, f"Interests: {', '.join(interests)}", ln=True)
    pdf.cell(0, 8, f"Travel Type: {travel_type}", ln=True)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Day-wise Plan", ln=True)

    pdf.set_font("Arial", size=12)

    for day, plan in itinerary_plan.items():
        pdf.ln(4)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, f"{day}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 7, plan)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output


# ---------------------------------------------------
# GENERATE ITINERARY
# ---------------------------------------------------
def generate_itinerary(city, days, interests):
    
    city_places = {
        "Mumbai": {
            "morning": [
                "Gateway of India + Ferry view",
                "Siddhivinayak Temple",
                "Colaba Causeway shopping",
                "Elephanta Caves ferry ride"
            ],
            "afternoon": [
                "Marine Drive walk",
                "Bandra-Worli Sea Link drive",
                "Juhu Chowpatty street food",
                "Haji Ali Dargah visit"
            ],
            "evening": [
                "Sunset at Marine Drive",
                "Nightlife in Bandra",
                "Shopping at Palladium Mall",
                "Versova beach walk"
            ]
        },

        "Hyderabad": {
            "morning": [
                "Charminar + Laad Bazaar",
                "Salar Jung Museum",
                "Chowmahalla Palace"
            ],
            "afternoon": [
                "Golconda Fort exploration",
                "Hussain Sagar Lake boating",
                "Birla Mandir temple"
            ],
            "evening": [
                "Ramoji Film City shows",
                "Necklace Road walk",
                "Hyderabadi biryani dinner at Paradise"
            ]
        },

        "London": {
            "morning": [
                "London Eye",
                "Buckingham Palace changing of guards",
                "Westminster Abbey tour"
            ],
            "afternoon": [
                "Tower Bridge + Tower of London",
                "British Museum",
                "Thames River cruise"
            ],
            "evening": [
                "Piccadilly Circus walk",
                "Covent Garden dining",
                "West End musical show"
            ]
        },

        "Edinburgh": {
            "morning": [
                "Edinburgh Castle",
                "Holyrood Palace",
                "Calton Hill sunrise"
            ],
            "afternoon": [
                "Royal Mile walking tour",
                "National Museum of Scotland",
                "Camera Obscura visit"
            ],
            "evening": [
                "Arthur’s Seat sunset",
                "Old Town ghost tour",
                "Traditional Scottish pub dinner"
            ]
        }
    }

    # Default fallback if city not found
    if city not in city_places:
        city_places[city] = {
            "morning": ["City exploration"],
            "afternoon": ["Local markets"],
            "evening": ["Cultural spots"]
        }

    itinerary = {}

    for day in range(1, days + 1):
        itinerary[f"Day {day}"] = (
            f"Morning: {random.choice(city_places[city]['morning'])}\n"
            f"Afternoon: {random.choice(city_places[city]['afternoon'])}\n"
            f"Evening: {random.choice(city_places[city]['evening'])}\n"
            f"Interest Match: {', '.join(interests)}"
        )

    return itinerary


# ---------------------------------------------------
# CREATE ITINERARY
# ---------------------------------------------------
itinerary_plan = generate_itinerary(city, days, interests)

# ---------------------------------------------------
# DISPLAY ITINERARY
# ---------------------------------------------------
st.subheader("Your Suggested Itinerary")

for day, plan in itinerary_plan.items():
    st.markdown(f"### {day}")
    st.write(plan)
    st.markdown("---")

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
add_bg("images/bgitinerary.png")
# ---------------------------------------------------
# DOWNLOAD PDF BUTTON
# ---------------------------------------------------
st.subheader("Download Itinerary")

if st.download_button(
    label="Download Itinerary",
    data=create_pdf(
        city=city,
        country=country,
        days=days,
        budget=budget,
        interests=interests,
        travel_type=travel_type,
        itinerary_plan=itinerary_plan
    ),
    file_name="itinerary.pdf",
    mime="application/pdf"
):
    st.success("Your itinerary is downloading!")

#----------------------------------------------------
# LOGOUT BUTTON
#----------------------------------------------------
if st.button("Logout"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.switch_page("pages/1_Login.py")


