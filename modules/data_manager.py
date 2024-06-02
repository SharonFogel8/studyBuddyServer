import streamlit as st

from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import json
import define
from modules import conversation_manager, pdf_handler
from gui import ui
# from gui import ui
from Objects.user_object import user
import login_page
from modules import text_processor


def import_conversation(chat_id):
    with st.spinner("Processing"):
        st.session_state.messages = []
        st.session_state.chat_history = convert_json_to_chat_history_format(st.session_state.my_user.uid, chat_id)
        text_chunks_db = login_page.get_texts_chanks_from_db(st.session_state.my_user.uid)
        text_to_vectore = ""
        for text_chunk in text_chunks_db.find({}):
            if text_chunk['session_id'] == chat_id:
                for text in text_chunk['text_chunks']:
                    text_to_vectore  += text
        st.session_state.my_user.update_current_chat(chat_id)
        text_chunks = text_processor.split_text_into_chunks(text_to_vectore)
        vectorstore = text_processor.create_vector_store(text_chunks)
        st.session_state.vectorstore = vectorstore
        st.session_state.text = text_to_vectore
        st.session_state.conversation = conversation_manager.get_conversation_chain(vectorstore)
        ui.show_chat()
        import_messages()


def import_messages():
    st.session_state.messages.clear()
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.session_state.messages.append({"role": "user", "content": message.content})
        else:
            response = f" {message.content}"
            st.session_state.messages.append({"role": "assistant", "content": response})



def import_questions(chat_id):
    question_history = login_page.get_questions_from_db(st.session_state.my_user.uid).find({})
    question = []
    for ques in question_history:
        if ques['session_id'] == chat_id:
            question.append(ques)

    st.session_state.questions = question

    ui.show_question()



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


def save_conversation_to_db(response):
    message_history = MongoDBChatMessageHistory(
        connection_string=define.CONNECTION_STRING, session_id=st.session_state.my_user.current_chat, database_name=define.CHATS,
        collection_name=st.session_state.my_user.uid)

    message_history.add_user_message(response["question"])
    message_history.add_ai_message(response["answer"])



def save_text_to_db(vectorestore):
    vectore_history = MongoDBAtlasVectorSearch(text_key=st.session_state.my_user.current_chat, embedding_key=st.session_state.my_user.uid, embedding=OpenAIEmbeddings())
    vectore_history.aadd_documents()


def save_text_chunks_to_db(text_chunks, pdf_files):
    db = login_page.get_texts_chanks_from_db(st.session_state.my_user.uid)
    names = pdf_handler.get_files_names(pdf_files)
    data_to_save = {
        "text_chunks": text_chunks,
        "session_id": st.session_state.my_user.current_chat,
        "user_id": st.session_state.my_user.uid,
        "file_name": names
    }

    # Insert data into MongoDB
    db.insert_one(data_to_save)


def save_questions_to_db(questions: dict, difficulty: str):
    db = login_page.get_questions_from_db(st.session_state.my_user.uid)
    data_to_save = questions

    # Insert data into MongoDB
    db.insert_one(data_to_save)


def get_file_names_from_db():
    text_chunks_db = login_page.get_texts_chanks_from_db(st.session_state.my_user.uid).find({})
    names = []
    for it in text_chunks_db:
        if it['session_id'] == st.session_state.my_user.current_chat:
            names.append(it['file_name'])
    return names