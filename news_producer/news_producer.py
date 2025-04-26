# news_producer.py
from kafka import KafkaProducer
import feedparser
import json
import time
from datetime import datetime, timezone

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka topic for news
topic = 'news_data'

# RSS Feeds you want to scrape
rss_feeds = [
    'https://finance.yahoo.com/rss/topstories',     # Yahoo Finance Top Stories
    'https://www.investing.com/rss/news_25.rss'      # Investing.com Financial News
]

def fetch_and_send_news():
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
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
        time.sleep(60)  # Wait for 1 minute before fetching again
