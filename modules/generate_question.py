from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
import streamlit as st

def file_processing(question_gen):

    splitter_ques_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',
        chunk_size=10000,
        chunk_overlap=200
    )

    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    splitter_ans_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',
        chunk_size=1000,
        chunk_overlap=100
    )

    document_answer_gen = splitter_ans_gen.split_documents(
        document_ques_gen
    )

    return document_ques_gen, document_answer_gen

def llm_pipline(file_path, difficulty):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    llm_ques_gen_pipeline = ChatOpenAI(
        temperature = 0.3,
        model = "gpt-3.5-turbo"
    )
    prompt_template = """
        You are an expert at creating questions based on coding materials and documentation.
        Your goal is to prepare a coder or programmer for their exam and coding tests.
        You do this by asking questions about the text below:

        ------------
        {text}
        ------------

        Create: {difficulty} difficulty questions that will prepare the coders or programmers for their tests.
        Make sure not to lose any important information.

        QUESTIONS:
        """

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text", "difficulty"])

    refine_template = ("""
        You are an expert at creating practice questions based on coding material and documentation.
        Your goal is to help a coder or programmer prepare for a coding test.
        We have received some practice questions to a certain extent: {existing_answer}.
        We have the option to refine the existing questions or add new ones.
        (only if necessary) with some more context below.
        ------------
        {text}
        ------------

        Given the new context, refine the original questions to be: {difficulty} difficulty in English.
        If the context is not helpful, please provide the original questions.
        QUESTIONS:
        """
                       )

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text", "difficulty"],
        template=refine_template,
    )

    ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline,
                                          chain_type="refine",
                                          verbose=True,
                                          question_prompt=PROMPT_QUESTIONS,
                                          refine_prompt=REFINE_PROMPT_QUESTIONS)

    ques = ques_gen_chain.run(input_documents=document_ques_gen, difficulty=difficulty)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

    ques_list = ques.split("\n")
    filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

    answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen,
                                                          chain_type="stuff",
                                                          retriever=vector_store.as_retriever())

    return answer_generation_chain, filtered_ques_list


def generate_ques(text_chunks, difficulty):
    answer_generation_chain, ques_list = llm_pipline(text_chunks, difficulty)
    answers = {}
    for question in ques_list:
        answer = answer_generation_chain.run(question)
        answers[question] = answer
    ques = {
        "questions": answers,
        "difficulty": difficulty,
        "session_id": st.session_state.my_user.current_chat,
        "user_id": st.session_state.my_user.uid
    }
    return ques


