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
from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

import define
from pages import login_page
import json
from Objects.user_object import user

# history_data = login_page.get_session_from_db('3c4550ec-f7a9-499e-8239-d472598526df')
# index = 0
# for chat in history_data:
#     # print(chat)
#     if (chat['SessionId'] == index):
#         dict_data = json.loads(chat['History'])
#         print(dict_data)
#         print(dict_data['data']['content'])

def convert_all_chats_to_dict(user_id: str):
    history_data = login_page.get_session_from_db(user_id)

    original_chat_history = []
    for message in history_data:
        history = json.loads(message['History'])
        print(message)
        if history['type'] == 'human':
            original_chat_history.append(HumanMessage(history['data']['content']))
        elif history['type'] == 'ai':
            original_chat_history.append(AIMessage(history['data']['content']))
    return original_chat_history

user_id = '683b8837-7a82-4c19-b9c5-6714d938f305'
chat_index = 0
# print(convert_all_chats_to_dict(user_id))

text_chunks_db = login_page.get_texts_chanks_from_db(user_id)
text_to_vectore = ""
print(text_chunks_db)
for text_chunk in text_chunks_db.find({}):
    if text_chunk['session_id'] == 0:
        for text in text_chunk['text_chunks']:
            text_to_vectore += text

print(text_to_vectore)
