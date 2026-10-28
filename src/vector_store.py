from pathlib import Path
from langchain_community.embeddings import FastEmbedEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from .config import QDRANT_URL, QDRANT_API_KEY

QDRANT_LOCAL_PATH = Path(__file__).resolve().parent.parent / "db_qdrant"
QDRANT_LOCAL_PATH.mkdir(parents=True, exist_ok=True)
CACHE_PATH = str(Path("D:/hf_cache"))
Path(CACHE_PATH).mkdir(parents=True, exist_ok=True)

# SINGLETON to fix lock error
_qdrant_client_instance = None
_embeddings_instance = None

def get_embeddings():
    global _embeddings_instance
    if _embeddings_instance is None:
        print(f"Using FREE FastEmbed at {CACHE_PATH}")
        _embeddings_instance = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            cache_dir=CACHE_PATH
        )
    return _embeddings_instance

def get_qdrant_client():
    global _qdrant_client_instance
    if _qdrant_client_instance is not None:
        return _qdrant_client_instance
    if QDRANT_URL and QDRANT_API_KEY:
        _qdrant_client_instance = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    else:
        _qdrant_client_instance = QdrantClient(path=str(QDRANT_LOCAL_PATH))
    return _qdrant_client_instance

def build_vectorstore(chunks):
    global _qdrant_client_instance
    _qdrant_client_instance = None  # release lock before rebuild
    emb = get_embeddings()
    print(f"Embedding {len(chunks)} chunks with FREE FastEmbed...")
    db = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=emb,
        path=str(QDRANT_LOCAL_PATH),
        collection_name="agentic_research",
        force_recreate=True
    )
    _qdrant_client_instance = db.client
    return db

def load_vectorstore():
    emb = get_embeddings()
    client = get_qdrant_client()
    try:
        cols = client.get_collections().collections
        if not any(c.name == "agentic_research" for c in cols):
            return None
    except:
        return None
    return QdrantVectorStore(client=client, collection_name="agentic_research", embedding=emb)