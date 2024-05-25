import streamlit as st
import os
import logging

from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import json
import define
from modules import json_handler,conversation_manager, buttons_actions
from gui import ui
from Objects.user_object import user
from pages import login_page
import pymongo

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

def show_chats(history_data: dict):
    ui.sidebar_chat_history(history_data)
#
def import_conversation(user_id, chat_id):
    # buttons_actions.process_button_clicked(history_data[define.PDF_FILES])
    st.session_state.chat_history = convert_json_to_chat_history_format(user_id, chat_id)
    ui.show_chat()

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
        print(f'history_data on convert func {chat}')
        if (chat['SessionId'] == chat_index):
            messages.append(json.loads(chat['History']))
    original_chat_history = []
    for message in messages:
        if message['type'] == 'human':
            original_chat_history.append(HumanMessage(message['data']['content']))
        elif message['type'] == 'ai':
            original_chat_history.append(AIMessage(message['data']['content']))
    print(original_chat_history)
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

def save_conversation_to_db(response, my_user: user):
    message_history = MongoDBChatMessageHistory(
        connection_string=define.CONNECTION_STRING, session_id=my_user.current_chat, database_name=define.CHATS,
        collection_name=my_user.uid)

    message_history.add_user_message(response["question"])
    message_history.add_ai_message(response["answer"])


# def get_conversation_from_db(user_id: str, chat_index: int):
#     history_data = login_page.get_session_from_db(user_id)
#
#     for chat in history_data:
#         if (chat['SessionId'] == chat_index):
#             dict_data = json.loads(chat['History'])
#             print(dict_data['data']['content'])

def save_text_to_db(vectorestore, my_user):
    vectore_history = MongoDBAtlasVectorSearch(text_key=my_user.current_chat, embedding_key=my_user.uid, embedding=OpenAIEmbeddings())
    vectore_history.aadd_documents()


def save_text_chunks_to_db(text_chunks, session_id, uid):
    client = pymongo.MongoClient(
        "mongodb+srv://noy4958:StudyBuddy@cluster0.ldrqjou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["mydatabase"]
    collection = db["mycollection"]

    # Convert data to dictionaries

    data_to_save = {
        "text_chunks": text_chunks,
        "session_id": session_id,
        "user_id": uid
    }

    # Insert data into MongoDB
    collection.insert_one(data_to_save)


