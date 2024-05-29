from Objects.chats import chat
import login_page
import random
import string
class user:
    def __init__(self, name: str, uid: str, mail: str):
        self.chats = {}
        self.name = name
        self.uid = uid
        self.mail = mail
        self.current_chat = 0

    def add_new_chat(self)-> str:
        characters = string.ascii_letters + string.digits
        random_id = ''.join(random.choice(characters) for i in range(8))
        new_chat = chat(id=random_id, user_id=self.uid)
        self.chats[random_id] = new_chat
        self.current_chat = new_chat.id
        return new_chat.id


    def add_chat_by_id(self, chat_id):
        new_chat = chat(id=chat_id, user_id=self.uid)
        self.chats[chat_id] = new_chat

    def update_current_chat(self, chat_id: int):
        self.current_chat = chat_id

    def update_session_from_db(self):
        history_data = login_page.get_session_from_db(self.uid)
        for session in history_data:
            self.add_chat_by_id(session['SessionId'])

