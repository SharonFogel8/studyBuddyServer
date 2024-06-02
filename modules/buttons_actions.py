import streamlit as st
import define
from modules import conversation_manager, pdf_handler, text_processor, generate_question, data_manager
from gui import ui, htmlTemplates
from Objects.user_object import user


def create_button(*args, button_name: str, func_click):
    try:
        return st.button(button_name, on_click=func_click, args=args)
    except:
        print("button already created")


def summarized_clicked(vectorstore, text: str):
    create_button(vectorstore, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    st.session_state['user_input'] = "Summarize"
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response)
    ui.show_chat()
    if 'questions' in st.session_state:
        ui.show_question()
    # init_user_question_input(my_user, vectorstore, text)
    show_session_option(vectorstore=vectorstore, raw_text=text, is_chat=False)


def chat_clicked(vectorstore, text: str):
    create_button(vectorstore, text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    st.write("Chat")
    st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)


def generate_questions_with_difficulty(vectorstore, raw_text, difficulty):
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    st.session_state.questions.append(generate_question.generate_ques(raw_text, difficulty))

    data_manager.save_questions_to_db(questions=st.session_state.questions[-1], difficulty=difficulty)
    if 'messages' in st.session_state:
        ui.show_chat()

    ui.show_question()
    show_session_option(vectorstore=vectorstore, raw_text=raw_text)


def generate_question_clicked(vectorstore, raw_text):
    if 'messages' in st.session_state:
        ui.show_chat()
    if 'questions' in st.session_state:
        ui.show_question()
    st.title("Generate Questions")

    # Display difficulty level buttons
    st.write("Select the difficulty level:")
    col1, col2, col3 = st.columns(3)  # Create two columns

    with col1:
        st.button('Easy', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text), kwargs={'difficulty': 'easy'})
    with col2:
        st.button('Medium', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text), kwargs={'difficulty': 'medium'})
    with col3:
        st.button('Hard', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text),
                  kwargs={'difficulty': 'hard'})


def process_button_clicked(pdf_docs):
    with st.spinner("Processing"):
        print("processing")
        try:
            raw_text = pdf_handler.extract_text_from_pdfs(pdf_docs)
        except:
            st.error(" ⚠️ There is an Error with the file, Please upload PDF file! ")
            return
        text_chunks = text_processor.split_text_into_chunks(raw_text)
        vectorstore = text_processor.create_vector_store(text_chunks)
        st.session_state.vectorstore = vectorstore
        st.session_state.text = raw_text
        st.session_state.my_user.add_new_chat()
        data_manager.save_text_chunks_to_db(text_chunks, pdf_docs)
        st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    st.session_state.new_chat = False
    ui.show_file_names()
    show_session_option(vectorstore=vectorstore, raw_text=raw_text)


def show_session_option(vectorstore, raw_text, is_chat=False, is_summarize=True):
    if is_chat:
        create_button(vectorstore, raw_text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)

    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        create_button(vectorstore, raw_text, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    with col2:
        create_button(vectorstore, raw_text,button_name=define.GENERATE_QUESTION_BUTTON,
                  func_click=generate_question_clicked)


def check_status():
    if st.session_state.new_chat == True:
        st.session_state.new_chat = False
        create_process_button()
    elif st.session_state.user_input:
        get_user_question(vectoresotre=st.session_state.vectorstore, text=st.session_state.text)


def click_on_exist_chat(chat_id: int):
    if 'messages' in st.session_state:
        st.session_state.messages.clear()
    if 'questions' in st.session_state:
        st.session_state.questions.clear()
    data_manager.import_conversation(chat_id=chat_id)
    data_manager.import_questions(chat_id=chat_id)
    show_session_option(vectorstore=st.session_state.vectorstore, raw_text=st.session_state.text, is_chat=False)


def create_process_button():
    if 'messages' in st.session_state:
        st.session_state.messages.clear()
    if 'questions' in st.session_state:
        st.session_state.questions.clear()

    pdf_docs = ui.get_uploaded_pdfs()

    create_button(pdf_docs, button_name=define.PROCESS_BUTTON, func_click=process_button_clicked)


def get_user_question(vectorstore, text: str):
    # if 'messages' in st.session_state:
    #     st.session_state.messages.clear()
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response)
    ui.show_chat()
    if 'questions' in st.session_state:
        ui.show_question()
    show_session_option(vectorstore=vectorstore,raw_text=text, is_chat=False)


def new_chat_button():
    create_button(button_name=define.NEW_CHAT_BUTTON,
                                  func_click=new_chat_clicked)


def new_chat_clicked():
    st.session_state.new_chat = True
    if 'messages' in st.session_state:
        st.session_state.messages.clear()
    if 'questions' in st.session_state:
        st.session_state.questions.clear()
