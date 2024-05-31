import streamlit as st
from dotenv import load_dotenv
# from gui import ui
from modules import buttons_actions
from gui import ui
from gui.htmlTemplates import css
from login_page import (login, cookies)
from Objects.user_object import user


def main():
    if "set_page" not in st.session_state:
        st.set_page_config(page_title="Study Buddy", page_icon=":books:")
        st.session_state.set_page = 1
    print('main')
    load_dotenv()
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if 'new_chat' not in st.session_state:
        st.session_state.new_chat = True

    login()
    if "username" in cookies:
        if user not in st.session_state:
            my_user = user(name=cookies["username"], uid=cookies["username"], mail='cookies["email"]')
            st.session_state.user = my_user
        else:
            my_user = st.session_state.user
        if st.session_state.new_chat == True:
            buttons_actions.create_process_button(my_user)
        elif prompt := st.chat_input("Ask a question about your documents:"):
            print(prompt)
            st.session_state.user_input = prompt
            buttons_actions.get_user_question(my_user=my_user, vectorstore=st.session_state.vectorstore,
                                              text=st.session_state.text)
        with st.sidebar:
            buttons_actions.new_chat_button(my_user)
            ui.sidebar_chat_history(my_user)



    st.write(css, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
