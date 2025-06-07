import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_KEY"

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages])

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(text, prompt="Summarize this:"):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt} {text}"}
        ],
        temperature=0.5,
        max_tokens=400
    )
    return response['choices'][0]['message']['content']

st.set_page_config(page_title="Doc Summarizer", layout="centered")

st.title("📄 AI Document Summarizer")

uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
raw_text = st.text_area("Or paste text here:")

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)
elif raw_text:
    text = raw_text
else:
    text = None

if text:
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
            st.subheader("🧠 Summary")
            st.write(summary)
