import requests

HN_SEARCH_BY_DATE = "https://hn.algolia.com/api/v1/search_by_date"

def search_stories(query: str, hits_per_page: int = 20, page: int = 0) -> list[dict]:
    params = {
        "query": query,
        "tags": "story",
        "hitsPerPage": hits_per_page,
        "page": page,
    }
    r = requests.get(HN_SEARCH_BY_DATE, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data.get("hits", [])
