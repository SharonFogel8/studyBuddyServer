import streamlit as st
import define
from modules import conversation_manager, ui, pdf_handler, text_processor, generate_question, data_manager

# from gui import ui
from Objects.user_object import user

def create_button(*args, button_name: str, func_click):
    st.button(button_name, on_click=func_click, args=args)

def summarized_clicked(vectorstore):
    create_button(vectorstore, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    st.session_state['user_input'] = "Summarize the files to half page"
    st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    conversation_manager.handle_user_input()

def chat_clicked(my_user, vectorstore):
    create_button(my_user, vectorstore, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    st.write("Chat")
    st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    init_user_question_input(my_user)

def generate_question_clicked(vectorstore, raw_text):
    create_button(vectorstore, button_name=define.GENERATE_QUESTION_BUTTON, func_click=generate_question_clicked)
    generate_question.generate_ques(raw_text)

def process_button_clicked(my_user: user ,pdf_docs):
    with st.spinner("Processing"):
        print("processing")
        print(pdf_docs)
        raw_text = pdf_handler.extract_text_from_pdfs(pdf_docs)
        text_chunks = text_processor.split_text_into_chunks(raw_text)
        print(text_chunks)
        vectorstore = text_processor.create_vector_store(text_chunks)
        my_user.add_new_chat()
        data_manager.save_text_chunks_to_db(text_chunks, my_user.current_chat, my_user.uid)
    create_button(vectorstore, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    create_button(my_user, vectorstore, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    create_button(vectorstore, raw_text, button_name=define.GENERATE_QUESTION_BUTTON, func_click=generate_question_clicked)


def click_on_exist_chat(my_user: user, chat_id: int):
    data_manager.import_conversation(my_user=my_user, chat_id=chat_id)


def create_process_button(my_user: user):
    pdf_docs = ui.get_uploaded_pdfs()
    print(f'pdf docs = {pdf_docs}')
    create_button(my_user, pdf_docs, button_name=define.PROCESS_BUTTON, func_click=process_button_clicked)

def get_user_question(my_user):
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response, my_user=my_user)
    init_user_question_input(my_user)

def new_chat_button(my_user: user):
    st.empty()
    create_button(my_user, button_name=define.NEW_CHAT_BUTTON,
                                  func_click=new_chat_clicked)

def new_chat_clicked(my_user: user):
    st.session_state.conversation = None
    st.session_state.chat_history = None
    # create_process_button(my_user)


def init_user_question_input(my_user):
    st.text_input("Ask a question about your documents:", on_change=get_user_question, key="user_input", args=(my_user, ))
    # prompt = st.chat_input("Ask a question about your documents:")
    # if prompt:
    #     st.session_state.user_input = prompt
    #     get_user_question(my_user)
