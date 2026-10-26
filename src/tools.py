
from .config import TAVILY_API_KEY
def web_search(query: str, max_results: int = 5):
    if not TAVILY_API_KEY:
        print("TAVILY_API_KEY not set, skipping web search")
        return []
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_API_KEY)
        results = client.search(query, max_results=max_results, include_answer=True)
        docs = []
        for r in results.get("results", []):
            docs.append({"content": r.get("content", ""), "source": r.get("url", ""), "title": r.get("title", "")})
        print(f"Web search found {len(docs)} results")
        return docs
    except Exception as e:
        print(f"Web search error: {e}")
        return []
