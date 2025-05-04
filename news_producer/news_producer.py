import os
import json
import time
import feedparser
from datetime import datetime, timezone
from kafka import KafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = 'news_data'

rss_feeds = [
    'https://finance.yahoo.com/rss/topstories',
    'https://www.investing.com/rss/news_25.rss'
]

def fetch_and_send_news():
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            print(f"⚠️ No entries found in feed: {feed_url}")
            continue

        for entry in feed.entries:
            news_item = {
                "source": feed.feed.get("title", "Unknown Source"),
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "timestamp": entry.get("published", datetime.now(timezone.utc).isoformat())
            }
            producer.send(topic, value=news_item)
            print(f"Sent News: {news_item}")

if __name__ == "__main__":
    while True:
        fetch_and_send_news()
        print("✅ Fetched and sent latest news batch.")
        time.sleep(60)
