import streamlit as st
import os
import logging
from dotenv import load_dotenv
from gui import ui
from modules import buttons_actions
from modules import data_manager
from gui.htmlTemplates import css
from pages.login_page import (login, cookies)
from Objects.user_object import user
from pages import login_page
import define


def main():
    st.set_page_config(page_title="Study Buddy", page_icon=":books:")
    print('main')
    load_dotenv()

    login()
    # print(st.session_state.username)
    # if not cookies.get():
    my_user = user(name=cookies["username"], uid=cookies["unique_key"], mail='cookies["email"]')
    buttons_actions.create_process_button(my_user)

    st.write(css, unsafe_allow_html=True)


    with st.sidebar:
        buttons_actions.new_chat_button(my_user)
        ui.sidebar_chat_history(my_user.uid)
        # data_manager.import_history_file()

#משימות שלא סיימתי : להחליט אם להשאיר את chats כlist או להפוך את זה לhash map ואז כששומרים שיחה צריך להחליט איך להגיד לו לאיזה שיחה להשתייך
# בתוך chats צריך להיות dict של History chat, summarize, QA
# לבדוק איך עושים רמת קושי לשאלות

if __name__ == '__main__':
    main()
