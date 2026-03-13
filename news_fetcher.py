import feedparser
from datetime import datetime, timezone
from dateutil import parser
from tqdm import tqdm

BASE_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_news(location="Global", query="latest news", hours=12, max_articles=5000):
    if location != "Global":
        query = f"{query} {location}"

    feed_url = BASE_URL.format(query=query.replace(" ", "+"))
    feed = feedparser.parse(feed_url)
    now = datetime.now(timezone.utc)

    news_list = []
    for entry in tqdm(feed.entries[:max_articles], desc=f"Fetching news for {location}"):
        try:
            published = parser.parse(entry.published)
            diff = (now - published).total_seconds() / 3600
            if diff <= hours:
                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published.strftime("%Y-%m-%d %H:%M"),
                    "summary": entry.summary if "summary" in entry else ""
                })
        except:
            continue
    return news_list