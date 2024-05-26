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
import streamlit as st
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

user_id = '683b8837-7a82-4c19-b9c5-6714d9f305'
chat_index = 0
# print(convert_all_chats_to_dict(user_id))
#
# text_chunks_db = login_page.get_texts_chanks_from_db(user_id)
# text_to_vectore = ""
# print(text_chunks_db)
# for text_chunk in text_chunks_db.find({}):
#     if text_chunk['session_id'] == 0:
#         for text in text_chunk['text_chunks']:
#             text_to_vectore += text
#
# print(text_to_vectore)

# his = login_page.get_session_from_db(user_id)
# if his.collection.count_documents({}) == 0:
#     print("nothing")
# for h in his:
#     print(h)
#
# history_data = login_page.get_session_from_db('f0be0a3d-c00f-4ed7-9fc6-e895c244daf5')
# print(f"history_data = {history_data}")
#
# if history_data.collection.count_documents({}) == 0:
#     print("empty")
#
# else:
#     #add if to empty history
#     index = 0
#     print("got here!")
#     for chat in history_data:
#         print(f"index = {index}")
#         if chat['SessionId'] >= index:
#             print(chat)
#             # my_user.add_chat_by_id(chat['SessionId'])
#             # st.sidebar.button(f"chat number {index}", on_click=buttons_actions.click_on_exist_chat, args=(my_user, chat['SessionId']))
#             # st.sidebar.write("---")
#             index +=1


def show_question(questions: dict):
    for ques, answer in questions.items():
        print(f"ques = {ques}")
        print(f"answer = {answer}")
#
# d = {"ques":"fdsdfsf", "fsdff": "fffff"}
# show_question(d)

import streamlit as st
import streamlit.components.v1 as components

import streamlit as st
import streamlit as st
import streamlit as st
import streamlit as st
from streamlit_carousel import carousel

# Define the questions and answers dictionary
qa_dict = {
    "מהי הבירה של ישראל?": "ירושלים",
    "מי היה הנשיא הראשון של ישראל?": "חיים ויצמן",
    "מהו הנהר הארוך ביותר בעולם?": "האמזונס"
}

# Define the templates for user and bot messages
def format_question_answer(question, answer):
    user_template = '''
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
    '''
    bot_template = '''
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
    '''
    return user_template.replace("{{MSG}}", question) + bot_template.replace("{{MSG}}",answer)

# List of images (one for each question-answer pair)
images = [
    "https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png",  # Example image URL
    "https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png",  # Example image URL
    "https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png"   # Example image URL
]

# Create a list of formatted question-answer pairs with titles, text, images, and empty links
slides = [
    {
        "title": question,
        "text": f"שאלה ותשובה {i + 1}",
        "content": f'<div style="text-align: center;"><h3>שאלה:</h3><p>{question}</p><h3>תשובה:</h3><p>{answer}</p></div>',
        "img": format_question_answer(question, answer),
        "link": "#"
    }
    for i, (question, answer) in enumerate(qa_dict.items())
]
# Display the carousel
# carousel(slides)
st.slider()

# Render the content using st.markdown
for slide in slides:
    st.markdown(slide["content"], unsafe_allow_html=True)