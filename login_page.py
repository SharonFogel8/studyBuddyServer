
import streamlit as st
import pymongo
from pymongo.server_api import ServerApi
import uuid
from streamlit_cookies_manager import EncryptedCookieManager
import define

# Initialize the cookie manager
cookies = EncryptedCookieManager(
    prefix="myapp_",
    password="study_buddy",
)

if not cookies.ready():
    st.stop()

# Connect to the DB.
@st.cache_resource
def connect_users_db():
    client = connect_db()
    db = client.get_database('main')
    return db.users

def connect_db():
    client = pymongo.MongoClient(
        "mongodb+srv://noy4958:StudyBuddy@cluster0.ldrqjou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1'))
    return client


def select_signup():
    st.session_state.form = 'signup_form'


def save_unique_key():
    unique_key = str(uuid.uuid4())
    cookies["unique_key"] = unique_key


def user_update(name: str):
    st.session_state.username = name
    save_unique_key()
    cookies["username"] = name


def update_unique_key():
    unique_key = str(uuid.uuid4())
    cookies["unique_key"] = unique_key


def get_user_name():
    return cookies["username"]


def get_user_email():
    return cookies["email"]


def get_user_uid():
    return cookies["unique_key"]


def get_session_from_db(uid: str):
    client = connect_db()
    db = client.get_database(define.CHATS)
    return db[uid].find({})

def get_session_from_db(uid: str):
    client = connect_db()
    db = client.get_database(define.CHATS)
    return db[uid].find({})

def get_texts_chanks_from_db(uid: str):
    client = connect_db()
    db = client["Texts"]
    return db[uid]

def get_questions_from_db(uid: str):
    client = connect_db()
    db = client["Questions"]
    return db[uid]


def login():
    user_db = connect_users_db()
    # Initialize Session States.
    if 'username' not in st.session_state:
        st.session_state.username = cookies.get("username", "")
    if 'form' not in st.session_state:
        st.session_state.form = ''

    if st.session_state.username != '':
        st.sidebar.write(f"Hello {st.session_state.username.upper()}")

    # Initialize Sign In or Sign Up forms
    if st.session_state.form == 'signup_form' and st.session_state.username == '':
        signup_form = st.sidebar.form(key='signup_form', clear_on_submit=True)
        new_username = signup_form.text_input(label='Enter Username*')
        new_user_email = signup_form.text_input(label='Enter Email Address*')
        new_user_pas = signup_form.text_input(label='Enter Password*', type='password')
        user_pas_conf = signup_form.text_input(label='Confirm Password*', type='password')
        note = signup_form.markdown('*required fields')
        signup = signup_form.form_submit_button(label='Sign Up')

        if signup:
            if '' in [new_username, new_user_email, new_user_pas]:
                st.sidebar.error('Some fields are missing')
            else:
                if user_db.find_one({'log': new_username}):
                    st.sidebar.error('Username already exists')
                elif user_db.find_one({'email': new_user_email}):
                    st.sidebar.error('Email is already registered')
                else:
                    if new_user_pas != user_pas_conf:
                        st.sidebar.error('Passwords do not match')
                    else:
                        user_update(new_username)
                        user_db.insert_one({'log': new_username, 'email': new_user_email, 'pass': new_user_pas})
                        st.sidebar.success('You have successfully registered!')
                        st.experimental_rerun()  # Refresh to update UI

    elif st.session_state.username == '':
        login_form = st.sidebar.form(key='signin_form', clear_on_submit=True)
        username = login_form.text_input(label='Enter Username')
        user_pas = login_form.text_input(label='Enter Password', type='password')
        login = login_form.form_submit_button(label='Sign In')

        if login:
            if user_db.find_one({'log': username, 'pass': user_pas}):
                user_update(username)
                st.experimental_rerun()  # Refresh to update UI
            else:
                st.sidebar.error("Username or Password is incorrect. Please try again or create an account.")
    else:
        logout = st.sidebar.button(label='Log Out')
        if logout:
            user_update('')
            cookies["username"] = ""
            update_unique_key()
            st.session_state.form = ''
            st.experimental_rerun()

    # 'Create Account' button
    if st.session_state.username == "" and st.session_state.form != 'signup_form':
        signup_request = st.sidebar.button('Create Account', on_click=select_signup)
