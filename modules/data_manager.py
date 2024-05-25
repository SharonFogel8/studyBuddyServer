import streamlit as st
import os
import logging

from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import define
from modules import json_handler,conversation_manager, buttons_actions
from gui import ui
from Objects.user_object import user
from pages import login_page

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
# def import_conversation(history_data):
#     try:
#         buttons_actions.process_button_clicked(history_data[define.PDF_FILES])
#         st.session_state.chat_history = conversation_manager.convert_json_to_chat_history_format(history_data)
#         ui.show_chat()
#     except:
#         print("no data yet")

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
#
# def convert_json_to_chat_history_format(chat_history_json):
#     original_chat_history = []
#     for message in chat_history_json[define.CHAT_HISTORY]:
#         if message['type'] == 'HumanMessage':
#             original_chat_history.append(HumanMessage(message['content']))
#         elif message['type'] == 'AIMessage':
#             original_chat_history.append(AIMessage(message['content']))
#     return original_chat_history

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

def save_text_to_db(vectorestore, my_user):
    vectore_history = MongoDBAtlasVectorSearch(text_key=my_user.current_chat, embedding_key=my_user.uid, embedding=OpenAIEmbeddings())
    vectore_history.aadd_documents()

