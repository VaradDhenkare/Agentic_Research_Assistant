import streamlit as st
from pathlib import Path
from src.loader import load_docs_from_folder
from src.chunker import chunk_docs
from src.vector_store import build_vectorstore, load_vectorstore
from src.graph import run_agentic_rag
from src.config import CHROMA_PATH

st.set_page_config(page_title="Agentic Research Assistant", layout="wide")

# FIX: Cache the DB - prevents "already accessed" lock
@st.cache_resource
def get_vectorstore():
    return load_vectorstore()

@st.cache_resource
def get_embeddings_cached():
    from src.vector_store import get_embeddings
    return get_embeddings()

st.title("Agentic Research Assistant")
st.caption("Self-correcting RAG | FREE FastEmbed | Qdrant on D drive")

with st.sidebar:
    st.header("1. Ingest")
    st.info(f"DB Path: {CHROMA_PATH}")
    folder_path = st.text_input("Folder path", value="D:\\rag-projects\\my-docs")
    if st.button("Ingest / Rebuild", type="primary"):
        if not Path(folder_path).exists():
            st.error(f"Not found: {folder_path}")
        else:
            # Clear cache before rebuild to release lock
            get_vectorstore.clear()
            with st.spinner("Loading docs..."):
                docs = load_docs_from_folder(folder_path)
                st.write(f"Loaded {len(docs)} pages")
            with st.spinner("Chunking + Embedding (FREE local, 1-2 min first time)..."):
                chunks = chunk_docs(docs)
                build_vectorstore(chunks)
            # Clear cache after rebuild so next query loads new DB
            get_vectorstore.clear()
            get_embeddings_cached.clear()
            st.success(f"Done! {len(chunks)} chunks embedded.")

st.header("Ask Anything")

# FIX: Use cached version here - NOT load_vectorstore()
db = get_vectorstore()
if not db:
    st.warning("No index yet. Ingest folder from sidebar. Web search will still work.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if q := st.chat_input("e.g., What is CRAG? or what does my PDF say?"):
    st.session_state.messages.append({"role":"user","content":q})
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        with st.spinner("Retrieve -> Grade -> [Web Search] -> Generate..."):
            result = run_agentic_rag(q)
            st.markdown(result.get("answer","No answer"))
            st.caption(f"Grade: {result.get('relevance')} | Web used: {len(result.get('web_docs',[]))>0}")
            st.session_state.messages.append({"role":"assistant","content":result.get("answer","")})