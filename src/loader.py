
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
ALLOWED_EXTS = {".pdf", ".txt", ".md"}
def load_docs_from_folder(folder_path: str) -> List[Document]:
    root = Path(folder_path)
    if not root.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    docs = []
    for f in root.rglob("*"):
        if f.suffix.lower() not in ALLOWED_EXTS:
            continue
        if f.stat().st_size > 10 * 1024 * 1024:
            continue
        try:
            if f.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(f))
                loaded = loader.load()
                for d in loaded:
                    d.metadata["source"] = str(f.relative_to(root))
                docs.extend(loaded)
            else:
                loader = TextLoader(str(f), encoding="utf-8")
                loaded = loader.load()
                for d in loaded:
                    d.metadata["source"] = str(f.relative_to(root))
                docs.extend(loaded)
        except Exception as e:
            print(f"Skipping {f}: {e}")
            continue
    print(f"Loaded {len(docs)} pages from {folder_path}")
    return docs
