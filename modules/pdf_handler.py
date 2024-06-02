from PyPDF2 import PdfReader

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
