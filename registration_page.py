import streamlit as st
from pymongo.mongo_client import MongoClient
import pandas as pd

st.title("USER INFORMATION")


def connect_to_mongo():
    user = st.secrets["username"]
    db_password = st.secrets["password"]

    # This is our database connection string, for a cluster called tb-ii
    uri = f"mongodb+srv://{user}:{db_password}@tb2.yubsq.mongodb.net/?retryWrites=true&w=majority&appName=TB2"

    # Let's connect to our MongoClient
    client = MongoClient(uri)

    return client


usernames = []


def registration_page():
    placeholder = st.empty()

    with placeholder.form("USER DATA"):
        user_name = st.text_input("Username")
        password = st.text_input("Choose a password", type="password")
        password2 = st.text_input("Repeat password", type="password")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if len(password) < 8:
            st.error("Password needs at least 8 characters", icon="🚨")
        elif len(user_name) < 1:
            st.error("Username needs at least 1 character", icon="🚨")
        elif password != password2:
            st.error("Passwords do not match", icon="🚨")
        else:
            client = connect_to_mongo()

            db = client["Streamlit"]
            collection = db["user_registration_data"]

            document = {f"user_name": user_name,
                        "password": password,
                        }

            collection.insert_one(document)

            placeholder.empty()
            st.title("Registration successful")
