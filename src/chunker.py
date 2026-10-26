
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", ". ", " ", ""])
    chunks = splitter.split_documents(docs)
    print(f"Chunked {len(docs)} docs into {len(chunks)} chunks")
    return chunks
