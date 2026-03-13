from news_fetcher import fetch_news
from article_extractor import extract_article
from vector_store import build_index

def create_store():
    locations = ["Global", "India"]  # removed Tamil Nadu, Chennai, Coimbatore
    texts = []
    for loc in locations:
        news = fetch_news(location=loc, hours=12, max_articles=1000)
        for article in news:
            text = extract_article(article["link"])
            if text:
                texts.append(text[:2000])
    if texts:
        build_index(texts)
        print(f"Vector store updated with {len(texts)} latest news articles!")

if __name__ == "__main__":
    create_store()