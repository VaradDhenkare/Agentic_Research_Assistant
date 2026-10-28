# 🔍 Agentic Research Assistant 

> A self-correcting RAG agent that knows when it doesn't know. If your local PDFs don't have the answer, it rewrites the query and searches the web.

**Project Level:** Moderate (RAG + Agents)  
**Stack:** LangGraph + Qdrant + Groq + Tavily  
**Disk Usage:** <200 MB, no Visual C++ Build Tools needed

---

## 🎯 What This Project Does

Implements **Corrective RAG (CRAG)**:

1. Retrieve from your local PDFs
2. **Grade** with LLM: Is the retrieved context relevant?
3. If **YES** → Generate answer with file citations
4. If **NO** → Rewrite query → Tavily web search → Generate with web + local citations

---

## ✨ Key Features

- No C++ compilation - uses Qdrant (pure Python)
- Citation aware: `[source: filename.pdf]` or `[source: https://...]`
- Agentic loop with LangGraph conditional edges
- Free tier ready: Groq (free) + FastEmbed local embeddings (100% free, CPU) + Tavily (1000 free/month)

---

## 📁 Folder Structure

```
Agentic-Research-Assistant/
├── app.py
├── cli.py
├── view_qdrant.py
├── db_qdrant/
├── requirements.txt
├── .env.example
├── README.md
└── src/
    ├── config.py
    ├── loader.py
    ├── chunker.py
    ├── vector_store.py
    ├── llm.py
    ├── web_search.py
    ├── grader.py
    ├── graph.py
    ├── prompts.py
    └── tools.py
```

---

## 🚀 Installation — For Anyone Downloading From GitHub

Works on Windows, macOS, and Linux.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/agentic-research-assistant.git
cd agentic-research-assistant
```

Or download ZIP from GitHub → Extract.

### 2. Activate Virtual Environment

**In this workspace (environment already set up):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
..\venvs\agentic\Scripts\Activate.ps1
```
*(You will see `(agentic)` in your terminal. All dependencies are already installed!)*

---

**Or if setting up fresh from GitHub:**

1. **Create Virtual Environment:**
   ```powershell
   # Windows
   python -m venv venv

   # macOS / Linux
   python3 -m venv venv
   ```

2. **Activate Virtual Environment:**
   ```powershell
   # Windows PowerShell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
   .\venv\Scripts\Activate.ps1

   # Windows CMD
   venv\Scripts\activate.bat

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

> No Visual C++ Build Tools needed - uses Qdrant (pure Python wheel) and FastEmbed.

### 3. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` in any editor and add your keys:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx
HF_HOME=D:\hf_cache
CHROMA_DB_PATH=db_qdrant
```

**API Keys Needed:**
- **Groq** (LLM, FREE): https://console.groq.com/keys — fast inference
- **Tavily** (web search, FREE): https://app.tavily.com — 1000 searches/month
- **FastEmbed** (Embeddings, 100% FREE): Runs entirely locally via `BAAI/bge-small-en-v1.5`, **no OpenAI API key needed!**

### 4. Add Your Documents

Create a folder for your PDFs:

```bash
mkdir my-docs
```

Put 5-10 PDFs, TXTs, or MDs inside `my-docs/` (or any folder you like).

### 5. Run the App

**Streamlit UI (Recommended):**

```bash
streamlit run app.py
```

Open http://localhost:8501

1. In sidebar, enter folder path: `./my-docs` or full path
2. Click **Ingest / Rebuild**
3. Ask questions in chat

**CLI Version:**

```bash
python cli.py ingest --path ./my-docs
python cli.py ask --q "What is our WFH policy?"
python cli.py ask --q "What is corrective RAG paper about?"
```

---

## 💬 Example Queries

**Local Hit (no web search needed):**
- "What does my PDF say about leave policy?"
- "Summarize the document about X"

**Local Miss → Web Fallback (uses web search):**
- "What is CRAG in RAG?"
- "Latest LangGraph features"

Check the debug expander in UI to see:
- `Relevance grade: relevant / irrelevant`
- `Web search used: True / False`

---

## ⚙️ Optional: Low C Drive Setup (Windows Users)

If you have low space on C drive, force caches to D drive:

```powershell
mkdir D:\hf_cache
mkdir D:\rag-projects\Agentic-Research-Assistant\db_qdrant
setx HF_HOME D:\hf_cache
setx CHROMA_DB_PATH D:\rag-projects\Agentic-Research-Assistant\db_qdrant
pip cache purge
```

Then set in `.env`:

```
CHROMA_DB_PATH=D:\rag-projects\Agentic-Research-Assistant\db_qdrant
```

Restart terminal after `setx`.

---
