import streamlit as st

from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import json
import define
from modules import conversation_manager, buttons_actions
from gui import ui
# from gui import ui
from Objects.user_object import user
import login_page
from modules import text_processor


#
# def import_history_file():
#     if os.path.exists(define.HISTORY_JASON_PATH):
#         logging.info("Import History")
#         print("Import History")
#         history_data = json_handler.load_json_to_argument(define.HISTORY_JASON_PATH)
#         show_chats(history_data)
#         import_conversation(history_data)
#     else:
#         logging.info("No history were found")
#         print("No history were found")
#         try:
#             os.makedirs(define.HISTORY_DIR_PATH)
#         except:
#             logging.info("history folder exist but empty")
#             print("history folder exist but empty")
#
#         if "conversation" not in st.session_state:
#             st.session_state.conversation = None
#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = None

# def show_chats_history(history_data: dict):
#     ui.sidebar_chat_history(history_data)


def import_conversation(chat_id):
    with st.spinner("Processing"):
        st.session_state.messages = []
        st.session_state.chat_history = convert_json_to_chat_history_format(st.session_state.my_user.uid, chat_id)
        text_chunks_db = login_page.get_texts_chanks_from_db(st.session_state.my_user.uid)
        text_to_vectore = ""
        for text_chunk in text_chunks_db.find({}):
            if text_chunk['session_id'] == chat_id:
                for text in text_chunk['text_chunks']:
                    text_to_vectore += text
        st.session_state.my_user.update_current_chat(chat_id)
        text_chunks = text_processor.split_text_into_chunks(text_to_vectore)
        vectorstore = text_processor.create_vector_store(text_chunks)
        st.session_state.vectorstore = vectorstore
        st.session_state.text = text_to_vectore
        st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
        ui.show_chat()
        import_messages()
        buttons_actions.show_session_option(vectorstore=vectorstore, raw_text=text_to_vectore, is_chat=False)
        # buttons_actions.init_user_question_input(vectorstore=vectorstore, my_user=my_user, text=text_to_vectore)

def import_messages():
    st.session_state.messages.clear()
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.session_state.messages.append({"role": "user", "content": message.content})
        else:
            response = f" {message.content}"
            st.session_state.messages.append({"role": "assistant", "content": response})


def import_questoions(chat_id):
    question_history = login_page.get_questions_from_db(st.session_state.my_user.uid).find({})
    question = {}
    for ques in question_history:
        if ques['session_id'] == chat_id:
            question.update(ques['questions'])

    st.session_state.questions = question
    ui.show_question(question)


    # def save_conversation(chat_index: int):
#     response_json = json_handler.load_json_to_argument(define.HISTORY_JASON_PATH)
#     response_json[define.CHATS][chat_index][define.CHAT_HISTORY] = convert_chat_history_to_json_format(st.session_state.chat_history)
#     json_handler.write_to_json(response_json, define.HISTORY_JASON_PATH)

# def save_pdf_files(pdf_docs, chat_index):
#     try:
#         json = json_handler.load_json_to_argument(define.HISTORY_JASON_PATH)
#         json[define.CHATS][chat_index][define.PDF_FILES] = pdf_docs
#     except:
#         json = {
#             define.CHATS[
#                 pdf_docs
#             ]
#         }
#     json_handler.write_to_json(json, define.HISTORY_JASON_PATH)

# def convert_chat_history_to_json_format(chat_history):
#     return [{'type': type(message).__name__, 'content': message.content} for message in chat_history]



def convert_json_to_chat_history_format(user_id, chat_index):
    messages = []
    history_data = login_page.get_session_from_db(user_id)
    # print(f'history_data on convert func {history_data}')
    for chat in history_data:
        if (chat['SessionId'] == chat_index):
            messages.append(json.loads(chat['History']))
    original_chat_history = []
    for message in messages:
        if message['type'] == 'human':
            original_chat_history.append(HumanMessage(message['data']['content']))
        elif message['type'] == 'ai':
            original_chat_history.append(AIMessage(message['data']['content']))
    print(f'original_chat_history = {original_chat_history}')
    return original_chat_history


def convert_all_chats_to_dict(user_id: str):
    history_data = login_page.get_session_from_db(user_id)
    original_chat_history = []
    for message in history_data:
        if message['type'] == 'human':
            original_chat_history.append(HumanMessage(message['data']['content']))
        elif message['type'] == 'ai':
            original_chat_history.append(AIMessage(message['data']['content']))
    return original_chat_history


# def save_new_chat():
#     try:
#         history_data = json_handler.load_json_to_argument(define.HISTORY_JASON_PATH)
#         history_data[define.CHATS].append({})
#     except:
#         history_data = {}
#         logging.info("new chat")
#     json_handler.write_to_json(history_data, define.HISTORY_JASON_PATH)


def save_conversation_to_db(response):
    message_history = MongoDBChatMessageHistory(
        connection_string=define.CONNECTION_STRING, session_id=st.session_state.my_user.current_chat, database_name=define.CHATS,
        collection_name=st.session_state.my_user.uid)

    message_history.add_user_message(response["question"])
    message_history.add_ai_message(response["answer"])


# def get_conversation_from_db(user_id: str, chat_index: int):
#     history_data = login_page.get_session_from_db(user_id)
#
#     for chat in history_data:
#         if (chat['SessionId'] == chat_index):
#             dict_data = json.loads(chat['History'])
#             print(dict_data['data']['content'])


def save_text_to_db(vectorestore):
    vectore_history = MongoDBAtlasVectorSearch(text_key=st.session_state.my_user.current_chat, embedding_key=st.session_state.my_user.uid, embedding=OpenAIEmbeddings())
    vectore_history.aadd_documents()


def save_text_chunks_to_db(text_chunks):
    db = login_page.get_texts_chanks_from_db(st.session_state.my_user.uid)

    data_to_save = {
        "text_chunks": text_chunks,
        "session_id": st.session_state.my_user.current_chat,
        "user_id": st.session_state.my_user.uid
    }

    # Insert data into MongoDB
    db.insert_one(data_to_save)


def save_questions_to_db(questions: dict, difficulty: str):
    db = login_page.get_questions_from_db(st.session_state.my_user.uid)

    data_to_save = {
        "questions": questions,
        "difficulty": difficulty,
        "session_id": st.session_state.my_user.current_chat,
        "user_id": st.session_state.my_user.uid
    }

    # Insert data into MongoDB
    db.insert_one(data_to_save)