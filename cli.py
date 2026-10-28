
import argparse
from src.loader import load_docs_from_folder
from src.chunker import chunk_docs
from src.vector_store import build_vectorstore
from src.graph import run_agentic_rag
def ingest(folder):
    docs = load_docs_from_folder(folder)
    chunks = chunk_docs(docs)
    build_vectorstore(chunks)
def ask(q):
    result = run_agentic_rag(q)
    print(result.get("answer"))
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["ingest","ask"])
    p.add_argument("--path", help="Folder path")
    p.add_argument("--q", help="Question")
    args = p.parse_args()
    if args.action == "ingest":
        ingest(args.path)
    else:
        ask(args.q)
