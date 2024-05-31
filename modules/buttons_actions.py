import streamlit as st
import define
from modules import conversation_manager, pdf_handler, text_processor, generate_question, data_manager
from gui import ui
from Objects.user_object import user

def create_button(*args, button_name: str, func_click):
    st.button(button_name, on_click=func_click, args=args)


def summarized_clicked(vectorstore, text: str):
    create_button(vectorstore, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    st.session_state['user_input'] = "Summarize"
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response)
    ui.show_chat()
    # init_user_question_input(my_user, vectorstore, text)
    show_session_option(vectorstore=vectorstore, raw_text=text, is_chat=False, is_summarize=False)


def chat_clicked(vectorstore, text: str):
    create_button(vectorstore, text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    st.write("Chat")
    st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    # init_user_question_input(my_user, vectorstore, text)
    # show_session_option(vectorstore=vectorstore, my_user=my_user, raw_text=text, is_chat=False)


# def generate_question_clicked(vectorstore, raw_text, my_user: user):
#     answers = generate_question.generate_ques(raw_text)
#     data_manager.save_questions_to_db(session_id=my_user.current_chat, questions=answers,uid=my_user.uid)
#     click_on_exist_chat(my_user=my_user, chat_id=my_user.current_chat)
def generate_questions_with_difficulty(vectorstore, raw_text,difficulty):

    print("----------" + difficulty)
    answers = generate_question.generate_ques(raw_text, difficulty)
    data_manager.save_questions_to_db(questions=answers,difficulty=difficulty)
    ui.show_question(answers)


def generate_question_clicked(vectorstore, raw_text):
    st.title("Generate Questions")
    create_button(vectorstore, button_name=define.GENERATE_QUESTION_BUTTON, func_click=generate_question_clicked)

    # Display difficulty level buttons
    st.write("Select the difficulty level:")

    st.button('Easy', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text), kwargs={'difficulty': 'easy'})
    st.button('Medium', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text), kwargs={'difficulty': 'medium'})
    st.button('Hard', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text), kwargs={'difficulty': 'hard'})

def process_button_clicked(pdf_docs):
    with st.spinner("Processing"):
        print("processing")
        raw_text = pdf_handler.extract_text_from_pdfs(pdf_docs)
        text_chunks = text_processor.split_text_into_chunks(raw_text)
        vectorstore = text_processor.create_vector_store(text_chunks)
        st.session_state.vectorstore = vectorstore
        st.session_state.text = raw_text
        st.session_state.my_user.add_new_chat()
        # st.session_state.my_user.update_session_from_db()
        data_manager.save_text_chunks_to_db(text_chunks)
        st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    st.session_state.new_chat = False
    show_session_option(vectorstore=vectorstore, raw_text=raw_text)
    # click_on_exist_chat(my_user=my_user, chat_id=my_user.current_chat)



def show_session_option(vectorstore, raw_text, is_chat=False, is_summarize=True):
    if is_chat:
        create_button(vectorstore, raw_text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    if is_summarize:
        create_button(vectorstore, raw_text, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    create_button(vectorstore, raw_text,button_name=define.GENERATE_QUESTION_BUTTON,
                  func_click=generate_question_clicked)


def check_status():
    if st.session_state.new_chat == True:
        st.session_state.new_chat = False
        create_process_button()
    elif st.session_state.user_input:
        get_user_question(vectoresotre=st.session_state.vectorstore, text=st.session_state.text)



def click_on_exist_chat(chat_id: int):
    data_manager.import_conversation(chat_id=chat_id)
    data_manager.import_questoions(chat_id=chat_id)



def create_process_button():
    pdf_docs = ui.get_uploaded_pdfs()
    create_button(pdf_docs, button_name=define.PROCESS_BUTTON, func_click=process_button_clicked)


def get_user_question(vectorstore, text: str):
    # if 'messages' in st.session_state:
    #     st.session_state.messages.clear()
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response)
    # data_manager.import_conversation(my_user=my_user, chat_id=my_user.current_chat)
    ui.show_chat()
    if 'questions' in st.session_state:
        ui.show_question(st.session_state.questions)
    show_session_option(vectorstore=vectorstore,raw_text=text, is_chat=False)
    # init_user_question_input(my_user, vectorstore, text)

def new_chat_button():
    create_button(button_name=define.NEW_CHAT_BUTTON,
                                  func_click=new_chat_clicked)


def new_chat_clicked():
    st.session_state.new_chat = True
    create_process_button()



# def init_user_question_input(my_user, vectorstore, text: str):
#     st.text_input("Ask a question about your documents:", on_change=get_user_question, key="user_input", args=(my_user, vectorstore, text))
