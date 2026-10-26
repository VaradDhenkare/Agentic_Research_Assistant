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
- Free tier ready: Groq (free) + OpenAI embeddings + Tavily (1000 free/month)

---

## 📁 Folder Structure

```
Agentic-Research-Assistant/
├── app.py
├── cli.py
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

### 2. Create Virtual Environment

**Windows (PowerShell / CMD):**
```powershell
python -m venv venv
```

**macOS / Linux:**
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal.

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> No Visual C++ Build Tools needed - uses Qdrant (pure Python wheel).

### 5. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` in any editor and add your keys:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj_xxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx
```

**Get Free API Keys:**
- **OpenAI** (embeddings): https://platform.openai.com/api-keys — `text-embedding-3-small` ~$0.02 for 50 PDFs
- **Groq** (LLM, FREE): https://console.groq.com/keys — `llama-3.3-70b-versatile`
- **Tavily** (web search, FREE): https://app.tavily.com — 1000 searches/month

### 6. Add Your Documents

Create a folder for your PDFs:

```bash
mkdir my-docs
```

Put 5-10 PDFs, TXTs, or MDs inside `my-docs/` (or any folder you like).

### 7. Run the App

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
mkdir D:\rag-projects\agentic-research\db_qdrant
setx HF_HOME D:\hf_cache
setx CHROMA_DB_PATH D:\rag-projects\agentic-research\db_qdrant
pip cache purge
```

Then set in `.env`:

```
CHROMA_DB_PATH=D:\rag-projects\agentic-research\db_qdrant
```

Restart terminal after `setx`.

---
