import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from gui import ui
# from gui import ui
import define



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_user_input():
    if st.session_state.user_input == '':
        return

    response = st.session_state.conversation({'question': st.session_state.user_input})
    st.session_state.chat_history = response[define.CHAT_HISTORY]

    return response

def handle_summarize():
    response = st.session_state.summarize({'question': st.session_state.user_input})
    st.session_state.summarize_history = response[define.CHAT_HISTORY][1]
    ui.show_chat()
    ui.show_summarize()
