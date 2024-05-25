# import modules.data_manager as data_manager
# import modules.json_handler as json_handler
# import os
#
# data = {
#     "Chats":[
#         {"chat_history": [
#     {
#         "type": "HumanMessage",
#         "content": "what dog eat?"
#     },
#     {
#         "type": "AIMessage",
#         "content": "Dogs should have a healthy balanced diet that meets their nutritional needs. They must have access to fresh clean drinking water at all times. It is advised to feed dogs at least once a day, but generally, it is better to feed them twice a day. Some dogs may have different dietary needs, so it's best to consult with a vet for advice on their specific diet."
#     },
#     {
#         "type": "HumanMessage",
#         "content": "how many time dog drink?"
#     },
#     {
#         "type": "AIMessage",
#         "content": "Dogs should have access to fresh clean drinking water at all times. It is important for their health and well-being. There isn't a specific number of times a dog should drink water, but they should have constant access to it throughout the day."
#     },
#     {
#         "type": "HumanMessage",
#         "content": "how many time dog eat?"
#     },
#     {
#         "type": "AIMessage",
#         "content": "Dogs should be fed at least once a day, but it is generally advised to feed them twice a day."
#     }
#
# ]}
# ]
# }
# os.mkdir('temp/')
# json_handler.write_to_json(data=data, json_path='temp/histort.json')
class chat:
    def __init__(self, id: str, user_id: str):
        self.id = id
        self.user_id = user_id

    # def add_file(self, file: list):
    #     self.files.append(file)

class user:
    def __init__(self, name: str, uid: str, mail: str):
        self.chats = []
        self.name = name
        self.uid = uid
        self.mail = mail

    def add_new_chat(self)-> int:
        new_chat = chat(id=len(self.chats), user_id=self.uid)
        self.chats.append(new_chat)
        return new_chat.id


my_user = user(name="kaka", uid="dsfdf", mail="dfsdf")
print(my_user.add_new_chat())
