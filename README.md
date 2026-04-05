# **📚 AskMyPDF — AI Chatbot 🤖**

### **Chat Seamlessly with Multiple PDFs!**
Transform how you interact with PDFs using **LangChain**, **Google Gemini**, and **FAISS Vector DB**!
Upload multiple PDFs, extract insights — including tables — and chat with them in real-time. 🚀✨

🔗 **[Try the Live Demo on Streamlit!](https://askmypdf1.streamlit.app/)**

---

## **📝 About AskMyPDF**

AskMyPDF is a **Streamlit-powered Retrieval-Augmented Generation (RAG) chatbot** that lets you upload multiple PDF files and engage in natural-language conversations with their content.

Using **Google Gemini Pro** for embeddings and answer generation, **FAISS** for local vector search, and **pdfplumber** for rich PDF extraction (including tables), it provides **instant and accurate responses** to your questions — grounded entirely in the documents you upload.

---

## **🎯 How It Works & Data Flow**

### **📌 Step-by-Step Execution Flow**
The entire process from document upload to answering a query:

1. **PDF Parsing (`pdfplumber`)**: When you upload PDFs, the app reads through every page extracting plain text and structured tabular data.
2. **Text Chunking**: Using `RecursiveCharacterTextSplitter`, the extracted text is segmented into chunks of `1000` characters, with `200` characters overlapping to ensure semantic meaning isn't lost at the boundaries.
3. **LLM Embeddings Generation**: These chunks are passed through Google's `gemini-embedding-001` model to generate numerical vector embeddings.
4. **FAISS Vector Storage**: The embeddings are persisted locally to disk using FAISS (Facebook AI Similarity Search) in a `faiss_index/` directory.
5. **Similarity Search**: When you ask a question, your query is also embedded, and the vector store performs a similarity search to fetch the top 4 most relevant chunks.
6. **Information Synthesis**: The context (the 4 chunks) and your query are passed into a prompt template, which is routed to Google's `gemini-2.5-flash` LLM, generating a precise response based purely on the context.

### **🗺️ Architecture System Flow**
```text
[ User Uploads PDFs ] 
      ↓ (pdfplumber Engine)
[ Text + Tables Extracted ]
      ↓ (RecursiveCharacterTextSplitter)
[ Chunks: 1000 chars & 200 overlap ]
      ↓ (gemini-embedding-001)
[ Vector Embeddings Array ]
      ↓ (FAISS Local Persistence)
[ Vector DB: faiss_index/ ] 
      ↑ similarity_search() 
[ User Query Input ] → fetches Top-4 Chunks
      ↓ 
[ PromptTemplate: Context + Question ]
      ↓ (gemini-2.5-flash, temp=0.3)
[ Answer Synthesised & Outputted to Chat UI ]
```

---

## **🚀 Key Features**

✅ **Multi-PDF Conversational AI** – Process multiple PDFs simultaneously into one knowledge base.
✅ **Table Extraction & Presentation** – Extracts structured tables using `pdfplumber` and displays them cleanly via pandas/Streamlit DataFrames.
✅ **Smart Adaptive Chunking** – Context-aware text limits to keep LLM context pristine.
✅ **Powered by Google Gemini** – Latest fast execution using `gemini-2.5-flash`.
✅ **Persistent FAISS Vector DB** – Indexes are saved to disk! You won't need to re-process files after refreshing the page.
✅ **Source Reference Tracking** – Outputs feature expandable components to strictly refer to textual passages the LLM utilized.
✅ **Premium Dark UI** – Dedicated Custom CSS wrapper handling smooth UI/UX animations.

---

## **🔧 Complete Setup & Execution Guide**

Follow the steps below to setup the project perfectly on your local machine.

### **Step 1: Clone the Repository**
Open your terminal and pull the project source code locally to your machine.
```bash
# Clone the remote codebase to your machine
git clone https://github.com/shubhamr9172/AskMyPDF---AI-Chatbot.git

# Move into the newly created project directory
cd AskMyPDF---AI-Chatbot
```

### **Step 2: Install Required Dependencies**
It is highly recommended to use a virtual environment, but system installation works fine as well. Install all python requirements automatically.
```bash
# Install parsing tools, langchain wrappers, and Streamlit
pip install -r requirements.txt
```

### **Step 3: Setup Google Gemini API Keys**
You need an active Google MakerSuite / Google AI Studio token to interact with the LLMs.
1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Inside your project's root folder (`AskMyPDF---AI-Chatbot/`), create a brand new file named strictly: `.env`
3. Open `.env` in any text editor and paste the following line, replacing the placeholder with your actual key:
```env
# Do not add quotes around the key string
GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
```

### **Step 4: Launch the Streamlit Server**
Start the main application. 
*(Note: If it's your first time running, Streamlit might ask for your email. You can leave it blank and hit Enter).*
```bash
# Execute the Streamlit runner targeting the main python application
streamlit run chatapp.py
```
> The dashboard will instantly become available via **`http://localhost:8501`** in your browser.
> *Note: By clicking `Process Documents`, the application will create a default folder called `faiss_index/` in your root file tree locally.*

---

## **📌 Tech Stack & Dependencies**

| 📦 Module | 🔹 Responsible Role |
|---|---|
| **Streamlit** | Core interaction frontend rendering & local web-server execution. |
| **Google Gemini (`gemini-2.5-flash`)** | Core language reasoning capability rendering coherent string answers. |
| **Google Gemini (`gemini-embedding-001`)** | Floating point transformer representing knowledge embeddings. |
| **LangChain Core + Community** | Logic orchestration handling LCEL components and prompts. |
| **FAISS** | Indexing arrays for the semantic dense text vectors. |
| **pdfplumber / PyPDF2** | Interpreting byte-level PDF characters strictly. |
| **pandas** | Tabular structure normalization and output mapping. |

---

## **📜 License**

This project is licensed under the **MIT License**.

---

## **🚀 Connect with Me!**

📌 **If you find this project useful, drop a ⭐ on GitHub!**

[![GitHub](https://img.shields.io/badge/GitHub-shubhamr9172-blue?logo=github&logoColor=white)](https://github.com/shubhamr9172/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Shubham%20Vivek%20Reddy-blue?logo=linkedin)](https://www.linkedin.com/in/shubham-vivek-reddy/)

### **🔥 Ready to Chat with Your PDFs? Try AskMyPDF Now!** 🚀
