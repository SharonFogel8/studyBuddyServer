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
from langchain_core.messages import HumanMessage, AIMessage
import login_page
import json


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

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt, col2 = st.columns([4, 1])
if prompt := st.chat_input("What is up?"):

    # Display user message in chat message container
    print(prompt)
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
if col2.button("lala"):
    st.write("lala")

st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        border: none;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Custom Styled Button Example")

if st.button('Styled Button'):
    st.write('Styled Button clicked!')
else:
    st.write('Styled Button not clicked.')


# Adding custom HTML and CSS
st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        border: none;
        border-radius: 12px;
        display: flex;
        align-items: center;
    }
    .stButton>button>svg {
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Button with Icon Example")

html_button = """
    <button>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
            <path d="M10.854 5.854a.5.5 0 0 0-.708-.708L7.5 7.793 5.854 6.146a.5.5 0 1 0-.708.708l2 2a.5.5 0 0 0 .708 0l4-4z"/>
        </svg>
            Click me
        </button>
    """

# Displaying button
if st.markdown(f"<div class='stButton'>{html_button}</div>", unsafe_allow_html=True):
    st.write('Button with icon clicked!')
else:
    st.write('Button with icon not clicked.')

    # Adding custom CSS to align the button to the left
st.markdown("""
    <style>
    .left-align-button {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        width: 100%;
    }
    .stButton button {
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        border: none;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Button Alignment Example")

# Using a placeholder to insert the button with custom alignment
left_align_placeholder = st.empty()
with left_align_placeholder.container():
    # Using HTML and CSS to create the button
    st.markdown('<div class="left-align-button"><button class="stButton">Left Aligned Button</button></div>', unsafe_allow_html=True)

    # Creating an actual button for interaction
    if st.button('Hidden Button', key='real_button'):
        st.write('Button clicked!')

# JavaScript to simulate click on the real button
st.markdown("""
    <script>
    document.querySelector('.left-align-button .stButton').onclick = function() {
        document.querySelector('button[kind="primary"]').click();
    };
    </script>
    """, unsafe_allow_html=True)



st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }
    .stButton button {
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        border: none;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Button Alignment Example")

# Creating a container to hold the button and align it to the left
button_container = st.container()
with button_container:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button('Left Aligned Button'):
        st.write('Button clicked!')
    st.markdown('</div>', unsafe_allow_html=True)