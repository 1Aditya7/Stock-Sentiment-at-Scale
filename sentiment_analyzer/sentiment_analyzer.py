import os
import json
from kafka import KafkaConsumer, KafkaProducer
from transformers import pipeline

# Environment variable for Kafka broker
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Kafka topic names
NEWS_TOPIC = "news_data"
SENTIMENT_TOPIC = "sentiment_data"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    NEWS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="sentiment-analyzer-group"
)

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Initialize BERT sentiment pipeline
bert_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(news):
    title = news.get("title", "")
    results = bert_analyzer(title)
    
    label = results[0]['label'].lower()  # returns 'positive', 'negative'
    score = results[0]['score']

    return {
        "source": news.get("source", ""),
        "title": title,
        "link": news.get("link", ""),
        "timestamp": news.get("timestamp", ""),
        "sentiment": label,
        "sentiment_score": round(score, 4)
    }

if __name__ == "__main__":
    print("🤖 BERT Sentiment Analyzer Running...")

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
