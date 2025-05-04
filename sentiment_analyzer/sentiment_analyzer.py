import os
import json
from kafka import KafkaConsumer, KafkaProducer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Environment variable for Kafka broker
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Kafka topic names
NEWS_TOPIC = "news_data"
SENTIMENT_TOPIC = "sentiment_data"

# Initialize Kafka consumer and producer
consumer = KafkaConsumer(
    NEWS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="sentiment-analyzer-group"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(news):
    title = news.get("title", "")
    scores = analyzer.polarity_scores(title)
    compound = scores.get("compound", 0.0)

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "source": news.get("source", ""),
        "title": title,
        "link": news.get("link", ""),
        "timestamp": news.get("timestamp", ""),
        "sentiment": label,
        "sentiment_score": round(compound, 4)
    }

if __name__ == "__main__":
    print("🧠 Sentiment analyzer running...")

    try:
        for msg in consumer:
            news_item = msg.value
            try:
                sentiment = analyze_sentiment(news_item)
                producer.send(SENTIMENT_TOPIC, value=sentiment)
                print(f"📊 Sent Sentiment: {sentiment}")
            except Exception as e:
                print(f"❌ Error processing message: {e} | Message: {news_item}")
    except KeyboardInterrupt:
        print("🛑 Shutting down analyzer.")
    except Exception as e:
        print(f"🚨 Fatal error in sentiment analyzer: {e}")
