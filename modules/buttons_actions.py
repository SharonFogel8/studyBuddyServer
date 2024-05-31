import streamlit as st
import define
from modules import conversation_manager, ui, pdf_handler, text_processor, generate_question, data_manager
from Objects.user_object import user

def create_button(*args, button_name: str, func_click):
    st.button(button_name, on_click=func_click, args=args)


def summarized_clicked(vectorstore, my_user: user, text: str):
    create_button(vectorstore, my_user, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    st.session_state['user_input'] = "Summarize"
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response, my_user=my_user)
    init_user_question_input(my_user, vectorstore, text)
    show_session_option(vectorstore=vectorstore, my_user=my_user, raw_text=text, is_chat=False, is_summarize=False)


def chat_clicked(my_user: user, vectorstore, text: str):
    create_button(my_user, vectorstore, text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    st.write("Chat")
    st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
    init_user_question_input(my_user, vectorstore, text)
    # show_session_option(vectorstore=vectorstore, my_user=my_user, raw_text=text, is_chat=False)


# def generate_question_clicked(vectorstore, raw_text, my_user: user):
#     create_button(vectorstore, button_name=define.GENERATE_QUESTION_BUTTON, func_click=generate_question_clicked)
#     answers = generate_question.generate_ques(raw_text)
#     data_manager.save_questions_to_db(session_id=my_user.current_chat, questions=answers,uid=my_user.uid)
#     ui.show_question(answers)

def generate_questions_with_difficulty(vectorstore, raw_text, my_user,difficulty):

    print("----------" + difficulty)
    answers = generate_question.generate_ques(raw_text, difficulty)
    data_manager.save_questions_to_db(session_id=my_user.current_chat, questions=answers, uid=my_user.uid,difficulty=difficulty)
    ui.show_question(answers)


def generate_question_clicked(vectorstore, raw_text, my_user: user):
    st.title("Generate Questions")
    create_button(vectorstore, button_name=define.GENERATE_QUESTION_BUTTON, func_click=generate_question_clicked)

    # Display difficulty level buttons
    st.write("Select the difficulty level:")

    st.button('Easy', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text, my_user), kwargs={'difficulty': 'easy'})
    st.button('Medium', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text, my_user), kwargs={'difficulty': 'medium'})
    st.button('Hard', on_click=generate_questions_with_difficulty, args=(vectorstore, raw_text, my_user), kwargs={'difficulty': 'hard'})

    # create_button(vectorstore, raw_text,difficulty='medium',my_user, button_name='Medium', func_click=generate_questions_with_difficulty)
    # create_button(vectorstore, raw_text, difficulty='hard',my_user, button_name='Hard', func_click=generate_questions_with_difficulty)
    
    # if col1.button('Easy'):
    #     st.session_state.difficulty = 'easy'
    #     generate_questions_with_difficulty(vectorstore, raw_text, 'easy', my_user)
    # if col2.button('Medium'):
    #     difficulty = 'medium'
    #     generate_questions_with_difficulty(vectorstore, raw_text, difficulty, my_user)
    # if col3.button('Hard'):
    #     difficulty = 'hard'
    #     generate_questions_with_difficulty(vectorstore, raw_text, difficulty, my_user)




def process_button_clicked(my_user: user ,pdf_docs):
    with st.spinner("Processing"):
        print("processing")
        raw_text = pdf_handler.extract_text_from_pdfs(pdf_docs)
        text_chunks = text_processor.split_text_into_chunks(raw_text)
        vectorstore = text_processor.create_vector_store(text_chunks)
        my_user.update_session_from_db()
        print(my_user.chats)
        my_user.add_new_chat()
        print(my_user.current_chat)
        data_manager.save_text_chunks_to_db(text_chunks, my_user.current_chat, my_user.uid)
    show_session_option(vectorstore=vectorstore, my_user=my_user, raw_text=raw_text)


def show_session_option(vectorstore, my_user, raw_text, is_chat=True, is_summarize=True):
    print('show options')
    if is_chat:
        create_button(my_user, vectorstore, raw_text, button_name=define.CHAT_BUTTON, func_click=chat_clicked)
    if is_summarize:
        create_button(vectorstore, my_user, raw_text, button_name=define.SUMMARIZE_BUTTON, func_click=summarized_clicked)
    create_button(vectorstore, raw_text, my_user, button_name=define.GENERATE_QUESTION_BUTTON,
                  func_click=generate_question_clicked)


def click_on_exist_chat(my_user: user, chat_id: int):
    data_manager.import_conversation(my_user=my_user, chat_id=chat_id)
    data_manager.import_questoions(my_user=my_user, chat_id=chat_id)



def create_process_button(my_user: user):
    pdf_docs = ui.get_uploaded_pdfs()
    create_button(my_user, pdf_docs, button_name=define.PROCESS_BUTTON, func_click=process_button_clicked)


def get_user_question(my_user: user, vectorstore, text: str):
    response = conversation_manager.handle_user_input()
    data_manager.save_conversation_to_db(response=response, my_user=my_user)
    init_user_question_input(my_user, vectorstore, text)
    show_session_option(vectorstore=vectorstore, my_user=my_user, raw_text=text, is_chat=False)


def new_chat_button(my_user: user):
    st.empty()
    create_button(my_user, button_name=define.NEW_CHAT_BUTTON,
                                  func_click=new_chat_clicked)


def new_chat_clicked(my_user: user):
    st.session_state.conversation = None
    st.session_state.chat_history = None


def init_user_question_input(my_user, vectorstore, text: str):
    st.text_input("Ask a question about your documents:", on_change=get_user_question, key="user_input", args=(my_user, vectorstore, text))

