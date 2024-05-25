import streamlit as st
from gui.htmlTemplates import bot_template, user_template
import define
import modules.data_manager as data_manager

def render_header():
    st.markdown("<h1 style='text-align: center; color: black;'>Study Buddy</h1>", unsafe_allow_html=True)
    st.header("Study Buddy :books:")

def get_user_question_input():
    return st.text_input("Ask a question about your documents:")

def get_uploaded_pdfs():
    return st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)



def show_options(func_click_chat, vectorstore):
    if 'chat' not in st.session_state:
        st.session_state.chat = False
    st.button("chat", on_click=func_click_chat(vectorstore))

    # clicked_button = {}
    # for option in define.OPTIONS.keys():
    #     clicked_button[option] = st.button(define.OPTIONS[option], on_click=funcr, args=(a,d))
    # return clicked_button

def show_chat():
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    st.session_state.user_input = ''

def sidebar_chat_history(history_data: list):
    st.sidebar.title("Chat History")
    try:
        for chat in history_data[define.CHATS]:
            st.sidebar.button(chat[define.CHAT_HISTORY][0]["content"], on_click=data_manager.import_conversation, args=(chat,))
            st.sidebar.write("---")
    except:
        print("no chat yet")


