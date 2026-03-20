import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from app.core.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
def web_search(query: str, max_results: int = 5) -> list[dict]:
    """search web using tavily and return results"""
    try:
        response = tavily_client.search(query=query, max_results=max_results, search_depth = "advanced")
        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content")
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def scrape_url(url: str) -> dict:
    """scrape a url and return the content"""
    try:
        headers = {"USer-agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(seaprator="\n", strip=True)
        # limit to 2000 chars to save tokens
        return {"url": url, "content": text[:2000]}
    except Exception as e:
        return {"url": url, "error": str(e)}    

