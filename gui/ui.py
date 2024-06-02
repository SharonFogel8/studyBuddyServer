import json

import streamlit as st
from gui.htmlTemplates import bot_template, user_template
import login_page
from Objects.user_object import user
from modules import buttons_actions
from modules import data_manager

def render_header():
    st.markdown("<h1 style='text-align: center; color: black;'>Study Buddy</h1>", unsafe_allow_html=True)
    st.header("Study Buddy :books:")


def get_user_question_input():
    return st.text_input("Ask a question about your documents:")


def get_uploaded_pdfs():
    return st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)



# def show_options(func_click_chat, vectorstore):
#     if 'chat' not in st.session_state:
#         st.session_state.chat = False
#     st.button("chat", on_click=func_click_chat(vectorstore))

    # clicked_button = {}
    # for option in define.OPTIONS.keys():
    #     clicked_button[option] = st.button(define.OPTIONS[option], on_click=funcr, args=(a,d))
    # return clicked_button

# def show_chat():
#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
#
#     st.session_state.user_input = ''

def show_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.chat_message("user").markdown(message.content)
        else:
            response = f" {message.content}"
            with st.chat_message("assistant"):
                st.markdown(response)
    st.session_state.user_input = ''
    st.session_state.new_chat = False

# def show_question():
#     for question, answer in st.session_state.questions.items():
#         with st.expander(question):
#             st.write(answer)


def show_question():
    easy_questions = {}
    medium_questions = {}
    hard_questions = {}
    for questions in st.session_state.questions:
        if 'easy' in questions['difficulty']:
            easy_questions.update(questions['questions'])
        elif 'medium' in questions['difficulty']:
            medium_questions.update(questions['questions'])
        elif 'hard' in questions['difficulty']:
            hard_questions.update(questions['questions'])

    if easy_questions:
        st.subheader("Easy questions")
        for question, answer in easy_questions.items():

            with st.expander(question):
                st.write(answer)

    if medium_questions:
        st.subheader("Medium questions")
        for question, answer in medium_questions.items():
            with st.expander(question):
                st.write(answer)

    if hard_questions:
        st.subheader("Hard questions")
        for question, answer in hard_questions.items():
            with st.expander(question):
                st.write(answer)

def show_summarize():

    for i, message in enumerate(st.session_state.summarize_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)

    st.session_state.user_input = ''


def sidebar_chat_history():
    history_data = login_page.get_session_from_db(st.session_state.my_user.uid)
    question_data = login_page.get_questions_from_db(st.session_state.my_user.uid).find({})

    if history_data.collection.count_documents({}) == 0 and question_data.collection.count_documents({}) == 0:
        st.sidebar.title("Welcome to StuddyBuddy")
        return
    else:
        st.sidebar.title("Chat History")
        index = []
        for chat in history_data:
            if chat['SessionId'] not in index:
                index.append(chat['SessionId'])
                # my_user.add_chat_by_id(chat['SessionId'])
                st.sidebar.button(f"{json.loads(chat['History'])['data']['content']}", on_click=buttons_actions.click_on_exist_chat, args=(chat['SessionId'], ), key=chat['SessionId'])
                st.sidebar.write("---")

        for question in question_data:
            if question['session_id'] not in index:
                index.append(question['session_id'])
                st.sidebar.button(list(question["questions"].keys())[0], on_click=buttons_actions.click_on_exist_chat, args=(question['session_id'], ), key=question['session_id'])
                st.sidebar.write("---")

