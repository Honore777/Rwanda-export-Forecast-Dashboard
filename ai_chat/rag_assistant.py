# ----------------- IMPORTS -----------------
# Standard Python
import os
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

# Google Generative AI
import google.generativeai as genai

# Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store / loaders
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

# Document class
from langchain_core.documents import Document

# ----------------- CONFIG -----------------
load_dotenv()

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Google AI API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use absolute paths
VECTOR_DB_PATH = os.path.join(BASE_DIR, "chroma_laws_db")
PDF_FOLDER = os.path.join(BASE_DIR, "../laws_pdfs")


POPPLER_PATH = r"C:\Users\USER\Desktop\poppler-25.11.0\Library\bin"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Optional: path to Poppler for pdf2image
POPPLER_PATH = r"C:\Users\USER\Desktop\poppler-25.11.0\Library\bin"

# ----------------- OCR PDF LOADER -----------------
def load_law_pdfs_with_ocr():
    all_docs = []
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs in {PDF_FOLDER}")
    
    for file in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, file)
        print(f"Processing {file}...")
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        
        for i, page_image in enumerate(pages):
            text = pytesseract.image_to_string(page_image, lang="eng")
            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={"source": file, "page": i + 1}
                )
                all_docs.append(doc)
        print(f"  -> Loaded {len(pages)} pages from {file}")
    
    print(f"Total pages loaded: {len(all_docs)}")
    return all_docs

# ----------------- SPLITTING -----------------
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"Documents split into {len(chunks)} chunks")
    return chunks

# ----------------- VECTOR DB -----------------
def create_vector_db():
    docs = load_law_pdfs_with_ocr()
    chunks = split_documents(docs)
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL),
        persist_directory=VECTOR_DB_PATH
    )
    print("Vector DB created and saved successfully!")
    return vectordb

def load_vector_db():
    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    )
    print("Vector DB loaded successfully!")
    return vectordb

# ----------------- SEARCH & ANSWER -----------------
def search_laws_data(query, k=5):
    vectordb = load_vector_db()
    results = vectordb.similarity_search(query, k)
    return results

def answer_question(query):
    results = search_laws_data(query)
    context = "\n\n".join([r.page_content for r in results])

    ai_prompt = f"""
    You are an AI assistant specializing in Rwanda business laws.

    Use ONLY the following legal context from the documents:

    context:
    {context}

    User question:
    {query}

    Provide a clear, legally accurate explanation based strictly on the documents.
    If the answer is not in the documents, say so.
    """

    response = model.generate_content(ai_prompt)
    return response.text

# ----------------- MAIN -----------------
if __name__ == "__main__":
    if not os.path.exists(VECTOR_DB_PATH):
        print("Creating vector database...")
        create_vector_db()
    else:
        print("Vector database already exists. Loading...")

    while True:
        query = input("\nAsk a question about Rwanda business laws (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        answer = answer_question(query)
        print("\n--- AI Answer ---")
        print(answer)
