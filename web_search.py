from duckduckgo_search import DDGS

def search_web(query, max_results=10):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })
    return results