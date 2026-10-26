from typing import List
from langchain_core.documents import Document
from .config import TAVILY_API_KEY

def web_search(query: str) -> List[Document]:
    """Free web search - uses Tavily if key exists, else returns empty (so your PDFs still work)"""
    if not TAVILY_API_KEY:
        print("No TAVILY_API_KEY - skipping web search, using only PDFs")
        return []
    
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_API_KEY)
        print(f"Searching web for: {query}")
        results = client.search(query, max_results=3, search_depth="basic")
        
        docs = []
        for r in results.get('results', []):
            content = r.get('content', '')[:1000]
            url = r.get('url', '')
            docs.append(Document(page_content=content, metadata={"source": url}))
        
        print(f"Found {len(docs)} web docs")
        return docs
    except Exception as e:
        print(f"Web search failed: {e} - using only PDFs")
        return []