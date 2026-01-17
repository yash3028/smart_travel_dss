import streamlit as st
import requests
import urllib.parse

BACKEND_URL = "http://localhost:3001/api/auth"

st.title("Smart Travel DSS - Login")

# Initialize session state
if "logged_in" not in st.session_state:
    token = st.query_params.get("token")

    if token:
        st.session_state["jwt"] = urllib.parse.unquote(token)
        st.session_state["logged_in"] = True
        st.switch_page("pages/2_Destination.py")
    else:
        st.session_state["logged_in"] = False

# ----------------------------- LOGIN FUNCTION -----------------------------
def login_user(username_, password):
    url = f"{BACKEND_URL}/login"
    payload = {"username": username_, "password": password}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        token = data["token"]
        st.session_state["logged_in"] = True
        st.session_state["jwt"] = token
        st.query_params["token"] = token
        print("JWT:", token)
        print("JWT length:", len(token))
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
    username_ = st.text_input("Username",key="login_username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username_ and password:
            login_user(username_, password)
        else:
            st.error("Please fill all fields")

# ----------------------------- SIGNUP TAB -----------------------------
with tabs[1]:
    st.subheader("Create a New Account")
    username = st.text_input("Username",key="signup_username")
    email_su = st.text_input("Email", key="su_email")
    password_su = st.text_input("Password", type="password", key="su_pass")

    if st.button("Signup"):
        if username and email_su and password_su:
            signup_user(username, email_su, password_su)
        else:
            st.error("Please fill all fields")
