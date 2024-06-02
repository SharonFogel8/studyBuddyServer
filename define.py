import os

OPTIONS = {"chat":"Chat With Me", "QA": "Generate Question", "summarize":"Summarize my Doc"}

CONNECTION_STRING = "mongodb+srv://noy4958:StudyBuddy@cluster0.ldrqjou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

PROCESS_BUTTON = "Process"
GENERATE_QUESTION_BUTTON = "Generate Question"
SUMMARIZE_BUTTON = "Summarize"
CHAT_BUTTON = "Chat With Me"
NEW_CHAT_BUTTON = "New Chat"


CURRENT_DIR = os.getcwd()
HISTORY_DIR_PATH = os.path.join(CURRENT_DIR, 'history')
HISTORY_JASON_PATH = os.path.join(HISTORY_DIR_PATH, 'history.json')
CONVERSATION_JSON_PATH = os.path.join(HISTORY_DIR_PATH, 'conversation.json')
HISTORY_FILE_PATH = os.path.join(HISTORY_DIR_PATH, 'history.txt')
CONVERSATION = "conversation"
CHAT_HISTORY = "chat_history"
PDF_FILES = "pdf_files"
CHATS = "Chats"
IMAGES_DIR_PATH = os.path.join(CURRENT_DIR, 'images')
SMALL_LOGO_PATH = os.path.join(IMAGES_DIR_PATH, 'robot_head.png')
LOGO_PATH = os.path.join(IMAGES_DIR_PATH, 'big_logo3.png')