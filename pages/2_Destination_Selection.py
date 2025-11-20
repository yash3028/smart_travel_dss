import streamlit as st

# Only allow access if logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
    st.stop()

st.title("Destination Selection")
st.write(f"Welcome, {st.session_state['username']}!")

st.header("Choose Destination or Let Us Recommend One")

choice = st.radio("Select one:", ["Choose My Own Destination", "Help Me Choose (AI Recommendation)"])

if choice == "Choose My Own Destination":
    st.write("You will select country, city, days, and month.")
    # We'll implement this page next

else:
    st.write("We will recommend a destination using AI + DSS.")
    # AI page will be implemented next