import streamlit as st
import pandas as pd
import hashlib
import os

# ---------- Helper Functions ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    if os.path.exists("users.csv"):
        users = pd.read_csv("users.csv")
        hashed = hash_password(password)

        user = users[(users["username"] == username) & (users["password"] == hashed)]
        return not user.empty
    return False

def create_user(name, username, password):
    hashed = hash_password(password)
    new_user = pd.DataFrame([[name, username, hashed]], columns=["name", "username", "password"])

    if os.path.exists("users.csv"):
        users = pd.read_csv("users.csv")
        # check if username already exists
        if username in users['username'].values:
            return False

        users = pd.concat([users, new_user], ignore_index=True)
        users.to_csv("users.csv", index=False)
    else:
        new_user.to_csv("users.csv", index=False)
    return True

# ---------- Login Page UI ----------
st.title("Smart Travel Planner - Login")

page = st.selectbox("Choose Option:", ["Login", "Sign Up"])

# ------------------ LOGIN ------------------
if page == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_login(username, password):
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.switch_page("pages/2_Destination_Selection.py")
        else:
            st.error("❌ Incorrect username or password.")

# ------------------ SIGN UP ------------------
else:
    st.subheader("Create a New Account")

    name = st.text_input("Full Name")
    username = st.text_input("Choose Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        success = create_user(name, username, password)
        if success:
            st.success("Account created! Please return to Login page.")
        else:
            st.error("❌ Username already exists. Try a different one.")