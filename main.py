import streamlit as st
from dotenv import load_dotenv
# from gui import ui
from modules import buttons_actions, ui
from gui.htmlTemplates import css
from pages.login_page import (login, cookies)
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

    login()
    if "username" in cookies:
        if user not in st.session_state:
            my_user = user(name=cookies["username"], uid=cookies["username"], mail='cookies["email"]')
            st.session_state.user = my_user
        else:
            my_user = st.session_state.user
        buttons_actions.create_process_button(my_user)
        with st.sidebar:
            buttons_actions.new_chat_button(my_user)
            ui.sidebar_chat_history(my_user)


    st.write(css, unsafe_allow_html=True)



        # data_manager.import_history_file()

#משימות שלא סיימתי : להחליט אם להשאיר את chats כlist או להפוך את זה לhash map ואז כששומרים שיחה צריך להחליט איך להגיד לו לאיזה שיחה להשתייך
# בתוך chats צריך להיות dict של History chat, summarize, QA
# לבדוק איך עושים רמת קושי לשאלות

if __name__ == '__main__':
    main()
