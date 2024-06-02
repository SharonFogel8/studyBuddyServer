import streamlit as st
from dotenv import load_dotenv

import define
# from gui import ui
from modules import buttons_actions
from gui import ui
from gui.htmlTemplates import css
from login_page import (login, cookies)
from Objects.user_object import user
from PIL import Image


def main():
    small_logo = Image.open(define.SMALL_LOGO_PATH)
    logo = Image.open(define.LOGO_PATH)
    try:
        st.set_page_config(page_title="Study Buddy", page_icon=small_logo)
    except:
        print("welcome")

    print('main')
    load_dotenv()
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if 'new_chat' not in st.session_state:
        st.session_state.new_chat = True
    if 'questions' not in st.session_state:
        st.session_state.questions = []

    st.sidebar.image(logo)
    login()

    if "username" in cookies and cookies["username"] != '':
        if 'my_user' not in st.session_state:
            st.session_state.my_user = user(name=cookies["username"], uid=cookies["username"], mail='cookies["email"]')

        if st.session_state.new_chat == True:
            buttons_actions.create_process_button()

        elif prompt := st.chat_input("Ask a question about your documents:"):
            st.session_state.user_input = prompt
            buttons_actions.get_user_question(vectorstore=st.session_state.vectorstore,
                                              text=st.session_state.text)
        with st.sidebar:

            # buttons_actions.new_chat_button(my_user)
            buttons_actions.create_button(button_name=define.NEW_CHAT_BUTTON,
                          func_click=buttons_actions.new_chat_clicked)
            ui.sidebar_chat_history()



    st.write(css, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
