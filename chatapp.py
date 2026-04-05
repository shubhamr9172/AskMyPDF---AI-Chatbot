import streamlit as st
from PyPDF2 import PdfReader
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from pathlib import Path

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AskMyPDF", page_icon="✦", layout="wide")

# Inject CSS — split into separate st.markdown calls to avoid rendering issues
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">', unsafe_allow_html=True)

st.markdown("""
<style>
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0A0A0A !important;
    color: #E8E4DC !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

[data-testid="stSidebar"] {
    background: #0F0F0F !important;
    border-right: 1px solid #1A1A1A !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #C9A96E 0%, #8B6914 100%) !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-top: 1rem !important;
    transition: opacity 0.2s !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    opacity: 0.8 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #1A1A1A !important;
    margin: 1.5rem 0 !important;
}

[data-testid="stFileUploader"] {
    background: #141414 !important;
    border: 1px dashed #252525 !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}

[data-testid="stMainBlockContainer"] {
    padding: 3rem 4rem !important;
    max-width: 960px !important;
}

.stTextInput > div > div > input {
    background: #0F0F0F !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 12px !important;
    color: #E8E4DC !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.9rem 1.25rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #C9A96E !important;
    box-shadow: 0 0 0 3px rgba(201,169,110,0.07) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #2A2A2A !important;
}

[data-testid="stExpander"] {
    background: #0F0F0F !important;
    border: 1px solid #161616 !important;
    border-radius: 12px !important;
    margin-bottom: 0.6rem !important;
}

[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left: 2px solid #C9A96E !important;
    background: #0F0F0F !important;
    font-size: 0.82rem !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #0A0A0A; }
::-webkit-scrollbar-thumb { background: #1E1E1E; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #C9A96E; }

.hero {
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #141414;
}

.hero-eyebrow {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C9A96E;
    margin-bottom: 0.75rem;
    font-family: 'DM Sans', sans-serif;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.5rem !important;
    font-weight: 300 !important;
    color: #E8E4DC !important;
    line-height: 1.1 !important;
    margin-bottom: 0.75rem !important;
}

.hero-title-italic {
    color: #C9A96E;
    font-style: italic;
    font-family: 'Cormorant Garamond', serif;
}

.hero-subtitle {
    font-size: 0.88rem;
    color: #444;
    font-weight: 300;
    line-height: 1.7;
    font-family: 'DM Sans', sans-serif;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #0F0F0F;
    border: 1px solid #1A1A1A;
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.72rem;
    color: #555;
    margin-bottom: 2rem;
    letter-spacing: 0.06em;
    font-family: 'DM Sans', sans-serif;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #222;
    flex-shrink: 0;
}

.status-dot-active {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4CAF50;
    box-shadow: 0 0 8px rgba(76,175,80,0.5);
    flex-shrink: 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1.25rem;
    margin-top: 2rem;
}

.section-divider-line {
    flex: 1;
    height: 1px;
    background: #141414;
}

.section-divider-text {
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #333;
    white-space: nowrap;
    font-family: 'DM Sans', sans-serif;
}

.chat-user {
    background: #0F0F0F;
    border: 1px solid #1A1A1A;
    border-radius: 14px;
    border-bottom-right-radius: 3px;
    padding: 1.25rem 1.5rem;
    margin-left: 4rem;
    margin-bottom: 1rem;
    color: #C9A96E;
    font-size: 0.88rem;
    line-height: 1.75;
    animation: fadeUp 0.25s ease;
}

.chat-bot {
    background: #0D0D0D;
    border: 1px solid #161616;
    border-radius: 14px;
    border-bottom-left-radius: 3px;
    padding: 1.25rem 1.5rem 1.25rem 2.25rem;
    margin-right: 4rem;
    margin-bottom: 1rem;
    color: #B8B2A8;
    font-size: 0.88rem;
    line-height: 1.75;
    position: relative;
    animation: fadeUp 0.25s ease;
}

.chat-bot::before {
    content: "✦";
    position: absolute;
    left: 0.8rem;
    top: 1.4rem;
    font-size: 0.5rem;
    color: #C9A96E;
    opacity: 0.6;
}

.chat-label {
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    opacity: 0.4;
    font-family: 'DM Sans', sans-serif;
}

.source-card {
    background: #0A0A0A;
    border: 1px solid #141414;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-top: 0.4rem;
    font-size: 0.78rem;
    color: #3A3A3A;
    line-height: 1.65;
    font-style: italic;
}

.source-label {
    font-size: 0.58rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #252525;
    margin-bottom: 0.4rem;
    font-style: normal;
    font-family: 'DM Sans', sans-serif;
}

.sidebar-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #E8E4DC;
    letter-spacing: 0.02em;
    margin-bottom: 0.25rem;
}

.sidebar-eyebrow {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A96E;
    margin-bottom: 1.5rem;
    font-family: 'DM Sans', sans-serif;
}

.sidebar-section-label {
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #333;
    margin-bottom: 0.6rem;
    font-family: 'DM Sans', sans-serif;
}

.file-item {
    font-size: 0.75rem;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #141414;
    font-family: 'DM Sans', sans-serif;
}

.footer {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #111;
    text-align: center;
    font-size: 0.68rem;
    color: #222;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
}

.footer a { color: #2A2A2A; text-decoration: none; }
.footer a:hover { color: #C9A96E; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──

def clean_table_data(table):
    if not table or len(table) == 0:
        return None
    try:
        df = pd.DataFrame(table)
        if df.empty:
            return None
        cols = []
        count = {}
        header_row = df.iloc[0].values if any(df.iloc[0].notna()) else [f"Col_{i}" for i in range(len(df.columns))]
        if all(df.iloc[0].astype(str) == header_row.astype(str)):
            df = df.iloc[1:].reset_index(drop=True)
        for idx, col in enumerate(header_row):
            col_name = str(col) if (col is not None and str(col).strip() != "") else f"Col_{idx}"
            if col_name in count:
                count[col_name] += 1
                cols.append(f"{col_name}_{count[col_name]}")
            else:
                count[col_name] = 0
                cols.append(col_name)
        df.columns = cols
        df = df.replace(['', ' ', None, np.nan, 'None', 'NaN'], np.nan)
        df = df.dropna(how='all').dropna(axis=1, how='all')
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Table error: {str(e)}")
        return None

def extract_pdf_content(pdf_docs):
    text_content = ""
    tables_content = []
    for pdf in pdf_docs:
        try:
            with pdfplumber.open(pdf) as pdf_reader:
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content += text + "\n\n"
                    for table in page.extract_tables():
                        cleaned = clean_table_data(table)
                        if cleaned is not None and not cleaned.empty:
                            tables_content.append(cleaned)
        except Exception as e:
            st.error(f"Error processing {pdf.name}: {str(e)}")
    return text_content, tables_content

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    vs = FAISS.from_texts(text_chunks, embedding=embeddings)
    vs.save_local("faiss_index")

def get_chain():
    prompt_template = """Answer the question from the context below. If not found, say "Answer not available in the provided documents."

Context: {context}

Question: {question}

Answer:"""
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return prompt | model | StrOutputParser()

def run_query(user_question):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = db.similarity_search(user_question)
        context = "\n\n".join([d.page_content for d in docs])
        response = get_chain().invoke({"context": context, "question": user_question})

        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-label">You</div>
            {user_question}
        </div>
        <div class="chat-bot">
            <div class="chat-label">AskMyPDF</div>
            {response}
        </div>
        """, unsafe_allow_html=True)

        if docs:
            with st.expander("View source passages"):
                for i, doc in enumerate(docs[:2]):
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-label">Source {i+1}</div>
                        {doc.page_content[:400]}...
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-eyebrow">✦ Document Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">AskMyPDF</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label" style="margin-top:1.5rem;">Upload Documents</div>', unsafe_allow_html=True)

    pdf_docs = st.file_uploader("Upload", accept_multiple_files=True, type="pdf", label_visibility="collapsed")

    if pdf_docs:
        for pdf in pdf_docs:
            st.markdown(f'<div class="file-item">▪ &nbsp;{pdf.name}</div>', unsafe_allow_html=True)

    if st.button("Analyse Documents"):
        if pdf_docs:
            with st.spinner("Processing..."):
                raw_text, tables = extract_pdf_content(pdf_docs)
                if not raw_text and not tables:
                    st.warning("No extractable content found.")
                    st.session_state['processed'] = False
                    st.stop()
                chunks = get_text_chunks(raw_text)
                try:
                    get_vector_store(chunks)
                    st.session_state['extracted_text'] = raw_text
                    st.session_state['extracted_tables'] = tables
                    st.session_state['processed'] = True
                    st.success("Ready — ask your first question.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state['processed'] = False
        else:
            st.warning("Please upload PDF files first.")

    st.markdown("---")
    st.markdown('<div class="sidebar-section-label">Powered by Gemini · Streamlit</div>', unsafe_allow_html=True)


# ── Main ──
is_ready = st.session_state.get('processed', False)
dot_class = "status-dot-active" if is_ready else "status-dot"
status_text = "Documents ready · Ask a question below" if is_ready else "Upload documents from the sidebar to begin"

st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">✦ Intelligent Document Analysis</div>
    <div class="hero-title">Ask anything about your
        <span class="hero-title-italic"> documents</span>
    </div>
    <div class="hero-subtitle">
        Upload PDFs, extract insights, and get precise answers<br>powered by Google Gemini.
    </div>
</div>
<div class="status-badge">
    <div class="{dot_class}"></div>
    {status_text}
</div>
""", unsafe_allow_html=True)

if is_ready:
    if st.session_state.get('extracted_text') or st.session_state.get('extracted_tables'):
        st.markdown("""
        <div class="section-divider">
            <div class="section-divider-text">Extracted Content</div>
            <div class="section-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get('extracted_text'):
            with st.expander("📄 View extracted text"):
                st.text_area("", value=st.session_state.extracted_text, height=250, label_visibility="collapsed")

        if st.session_state.get('extracted_tables'):
            n = len(st.session_state.extracted_tables)
            with st.expander(f"📊 View extracted tables ({n} found)"):
                for i, table in enumerate(st.session_state.extracted_tables):
                    st.caption(f"Table {i+1}")
                    try:
                        st.dataframe(table, use_container_width=True)
                    except:
                        st.write(table.to_dict())
                    if i < n - 1:
                        st.markdown("---")

    st.markdown("""
    <div class="section-divider" style="margin-top:2.5rem;">
        <div class="section-divider-text">Ask a Question</div>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    user_question = st.text_input(
        "Question",
        placeholder="What would you like to know about your documents?",
        label_visibility="collapsed"
    )

    if user_question:
        run_query(user_question)

st.markdown("""
<div class="footer">
    <a href="github" target="_blank">
        AskMyPDF · Created by Omkar Adarsh Shinde
    </a>
</div>
""", unsafe_allow_html=True)