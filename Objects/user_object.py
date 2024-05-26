from Objects.chats import chat

class user:
    def __init__(self, name: str, uid: str, mail: str):
        self.chats = []
        self.name = name
        self.uid = uid
        self.mail = mail
        self.current_chat = 0

    def add_new_chat(self)-> int:
        new_chat = chat(id=len(self.chats), user_id=self.uid)
        self.chats.append(new_chat)
        self.current_chat = new_chat.id
        return new_chat.id


    def add_chat_by_id(self, chat_id):
        new_chat = chat(id=chat_id, user_id=self.uid)
        self.chats.insert(chat_id, new_chat)

    def update_current_chat(self, chat_id: int):
        self.current_chat = chat_id