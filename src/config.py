import os
from dotenv import load_dotenv
load_dotenv()

# Only GROQ is required - FREE
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # optional, for web search

# Qdrant - optional, if not set uses local D drive (FREE)
QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

# Model names
LLM_GROQ = "openai/gpt-oss-20b"
LLM_OPENAI = "gpt-4o-mini"  # dummy, not used, just to prevent ImportError

# DB path on D drive
CHROMA_PATH = os.getenv("CHROMA_PATH", "D:/rag-projects/agentic-research/db_qdrant")

def get_llm_provider():
    return "groq"