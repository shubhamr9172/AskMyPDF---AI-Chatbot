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

## **🎯 How It Works**

### **📌 Step-by-Step Process**
1️⃣ **Upload PDFs** – Drag and drop multiple PDF files into the sidebar.
2️⃣ **Text & Table Extraction** – `pdfplumber` extracts both plain text and structured tables from every page.
3️⃣ **Smart Text Chunking** – Documents are split into overlapping 1000-character chunks (200-char overlap) for context preservation.
4️⃣ **Vector Embeddings** – Google's **`gemini-embedding-001`** model converts each chunk into a vector embedding.
5️⃣ **FAISS Index** – Embeddings are stored in a local **FAISS** vector index, persisted to disk.
6️⃣ **Similarity Search** – On each question, the top-4 most relevant chunks are retrieved.
7️⃣ **Response Generation** – **`gemini-2.5-flash`** synthesises a grounded answer from the retrieved context.

### **🗺️ Architecture Flow**

```
PDF Files
  ↓ pdfplumber
Text + Tables
  ↓ RecursiveCharacterTextSplitter (1000 chars / 200 overlap)
Text Chunks
  ↓ gemini-embedding-001
Vector Embeddings
  ↓ FAISS (saved to faiss_index/)
Vector Index
  ↑ User Question → similarity_search → Top-4 Chunks
  ↓ Context + Question → PromptTemplate
LLM Chain (gemini-2.5-flash, temp=0.3)
  ↓ StrOutputParser
Answer → Streamlit Chat UI + Expandable Source Passages
```

---

## **🚀 Key Features**

✅ **Multi-PDF Conversational AI** – Chat with multiple PDFs simultaneously.
✅ **Table Extraction** – Extracts and displays structured tables from PDFs using `pdfplumber`.
✅ **Smart Adaptive Chunking** – Overlapping text segmentation for improved retrieval accuracy.
✅ **Powered by Google Gemini** – Uses `gemini-embedding-001` for embeddings and `gemini-2.5-flash` for answers.
✅ **FAISS Local Vector Store** – Fast, persistent similarity search — no re-embedding on page refresh.
✅ **Source Passage Viewer** – Every answer shows expandable source passages for full transparency.
✅ **Premium Dark UI** – Custom Streamlit design with dark mode, gold accents, and smooth animations.

---

## **🔧 Installation & Setup**

### **Prerequisites**
- Python 3.8+
- A Google API Key with Gemini access → [Get one here](https://makersuite.google.com/app/apikey)

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/shubhamr9172/AskMyPDF---AI-Chatbot.git
cd AskMyPDF---AI-Chatbot
```

### **2️⃣ Install Required Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up API Key**
Create a `.env` file in the project root and add:
```
GOOGLE_API_KEY=<your-api-key-here>
```

### **4️⃣ Run the Application**
```sh
streamlit run chatapp.py
```
> The app runs on `http://localhost:8501` by default. The `faiss_index/` directory is created automatically on first document processing.

---

## **💡 How to Use**

1️⃣ **Launch the App** – Run `streamlit run chatapp.py`.
2️⃣ **Upload PDFs** – Drag and drop multiple PDF files into the sidebar.
3️⃣ **Process Files** – Click **"Analyse Documents"** to extract text, tables, and build the vector index.
4️⃣ **Ask Questions** – Type your query in the chatbox and get AI-powered, context-grounded responses.
5️⃣ **Inspect Sources** – Expand **"View source passages"** to see exactly which parts of your PDFs were used.

---

## **📌 Tech Stack & Dependencies**

| 📦 Library / Service | 🔹 Role |
|---|---|
| **Streamlit** | Web UI framework |
| **Google Gemini** (`gemini-2.5-flash`) | LLM for answer generation |
| **Google Gemini** (`gemini-embedding-001`) | Vector embedding model |
| **LangChain** | RAG pipeline, prompt chaining, LCEL |
| **FAISS** | Local vector store for similarity search |
| **pdfplumber** | Rich PDF text & table extraction |
| **PyPDF2** | Fallback PDF parsing |
| **python-dotenv** | Secure API key management |
| **pandas / numpy** | Table cleaning and display |

---

## **📂 Project Structure**

```
AskMyPDF---AI-Chatbot/
├── chatapp.py            ← Main application entry point
├── requirements.txt      ← Python dependencies
├── .env                  ← API key storage (GOOGLE_API_KEY) — not committed
├── faiss_index/          ← Auto-generated FAISS vector index (persisted to disk)
├── img/                  ← Architecture & demo screenshots
├── docs/                 ← Supporting documentation assets
├── .devcontainer/        ← Dev container configuration
├── AskMyPdf_Workflow_Documentation.md  ← Full technical workflow documentation
├── .gitignore
└── README.md
```

---

## **🎯 Demo & Deployment**

Want to try AskMyPDF without any setup? 🚀

🔗 **[Try the Live App on Streamlit!](https://askmypdf1.streamlit.app/)**

---

## **🛠️ Future Enhancements**

🔹 **Chat history & memory** – Persist conversation context across turns.
🔹 **Streaming responses** – Progressive token rendering with `stream=True`.
🔹 **DOCX & PPTX support** – Expand beyond PDF documents.
🔹 **Table-aware embeddings** – Serialize table content and embed alongside PDF text.
🔹 **Named FAISS indices** – Support multiple document sets without overwriting.
🔹 **Authentication** – Multi-user login for shared deployments.

---

## **📜 License**

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## **🚀 Connect with Me!**

📌 **If you find this project useful, drop a ⭐ on GitHub!**

[![GitHub](https://img.shields.io/badge/GitHub-shubhamr9172-blue?logo=github&logoColor=white)](https://github.com/shubhamr9172/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Shubham%20Vivek%20Reddy-blue?logo=linkedin)](https://www.linkedin.com/in/shubham-vivek-reddy/)

---

### **🔥 Ready to Chat with Your PDFs? Try AskMyPDF Now!** 🚀
