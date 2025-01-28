import streamlit as st
from pymongo.mongo_client import MongoClient
import pandas as pd
from helpers import connect_to_collection
from registration_page import registration_page

st.title("LOGIN")


def connect_to_mongo():
    user = st.secrets["username"]
    db_password = st.secrets["password"]

    # This is our database connection string, for a cluster called tb-ii
    uri = f"mongodb+srv://{user}:{db_password}@tb2.yubsq.mongodb.net/?retryWrites=true&w=majority&appName=TB2"

    # Let's connect to our MongoClient
    client = MongoClient(uri)

    return client


def login_page():
    placeholder = st.empty()

    with placeholder.form("LOGIN"):
        st.write("Hello! Please enter your log info.")
        st.write("If this is your first time on my app then please click on the Register Button.")
        username = st.text_input("username")
        password = st.text_input("password")
        login_button = st.form_submit_button("Login")
        register_button = st.form_submit_button("Register")

    if register_button:
        placeholder.empty()
        registration_page()

    if login_button:
        connect_to_mongo()
        # connect to collection
        # define the database
        db_name = 'Streamlit'
        # define the collection
        collection_name = 'user_registration_data'
        collection = connect_to_collection(db_name, collection_name)

        # check username
        # read the data from the collection and identify user names
        user_registration_data = pd.DataFrame(list(collection.find()))
        user_names = list(user_registration_data.user_name)

        # check password
        if username in user_names:
            # this selects the password of the user that is entering information
            registered_password = list(user_registration_data[user_registration_data.user_name == username].password)[0]

            if password == registered_password:
                credentials_check = True
                placeholder.empty()
                st.title("Success")
            else:
                st.error("The username/password is not correct")
        else:
            st.error("Please provide correct user name or click on register as new user")
