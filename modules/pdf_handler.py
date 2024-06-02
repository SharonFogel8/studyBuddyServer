from PyPDF2 import PdfReader
from fpdf import FPDF
import streamlit as st

import define


def extract_text_from_pdfs(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_files_names(pdf_docs):
    names = []
    for pdf_file in pdf_docs:
        names.append(pdf_file.name)
    return names

def create_questions_file():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVuSansCondensed", fname=define.FONT_PATH, uni=True)
    pdf.set_font("DejaVuSansCondensed", size=12)

    for entry in st.session_state.questions:
        questions_and_answers = entry['questions']
        difficulty = entry['difficulty']
        pdf.multi_cell(200, 10, txt=difficulty)
        for question, answer in questions_and_answers.items():
            pdf.multi_cell(200, 10, txt=question)
            pdf.multi_cell(200, 10, txt=answer)
            pdf.ln(5)
    return pdf