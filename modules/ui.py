import streamlit as st
from gui.htmlTemplates import bot_template, user_template
import define
import modules.data_manager as data_manager
from pages import login_page
from Objects.user_object import user
from modules import buttons_actions

def render_header():
    st.markdown("<h1 style='text-align: center; color: black;'>Study Buddy</h1>", unsafe_allow_html=True)
    st.header("Study Buddy :books:")

def get_user_question_input():
    return st.text_input("Ask a question about your documents:")


def get_uploaded_pdfs():
    print("upload")
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
    print("show chat")
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    st.session_state.user_input = ''

def sidebar_chat_history(my_user: user):
    st.empty()
    history_data = login_page.get_session_from_db(my_user.uid)
    print(f"history_data = {history_data}")
    st.sidebar.title("Chat History")
    if history_data.collection.count_documents({}) == 0:
        print("empty")
        return
    else:
        #add if to empty history
        index = 0
        print("got here!")
        for chat in history_data:
            print(f"index = {index}")
            if chat['SessionId'] >= index:
                print(chat)
                my_user.add_chat_by_id(chat['SessionId'])
                st.sidebar.button(f"chat number {index}", on_click=buttons_actions.click_on_exist_chat, args=(my_user, chat['SessionId']))
                st.sidebar.write("---")
                index +=1



