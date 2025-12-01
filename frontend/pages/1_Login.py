import streamlit as st
import requests

BACKEND_URL = "http://localhost:3001/api/auth"

st.title("Smart Travel DSS - Login")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------- LOGIN FUNCTION -----------------------------
def login_user(email, password):
    url = f"{BACKEND_URL}/login"
    payload = {"email": email, "password": password}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        st.session_state.logged_in = True
        st.session_state.token = data.get("token", "")
        st.success("Login successful!")
        st.switch_page("pages/2_Destination.py")
    elif response.status_code == 401:
        st.error("Unauthorized: Wrong email or password")
    else:
        st.error("Backend error. Try again.")

# ----------------------------- SIGNUP FUNCTION -----------------------------
def signup_user(username, email, password):
    url = f"{BACKEND_URL}/save-user"
    payload = {"username": username, "email": email, "password": password}

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        st.success("Signup successful! You can now log in.")
    else:
        st.error("Signup failed. Try another email.")

# ----------------------------- UI SWITCHER -----------------------------
tabs = st.tabs(["Login", "Signup"])

# ----------------------------- LOGIN TAB -----------------------------
with tabs[0]:
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            login_user(email, password)
        else:
            st.error("Please fill all fields")

# ----------------------------- SIGNUP TAB -----------------------------
with tabs[1]:
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    email_su = st.text_input("Email", key="su_email")
    password_su = st.text_input("Password", type="password", key="su_pass")

    if st.button("Signup"):
        if username and email_su and password_su:
            signup_user(username, email_su, password_su)
        else:
            st.error("Please fill all fields")
