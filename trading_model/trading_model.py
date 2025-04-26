# trading_model.py
from kafka import KafkaConsumer, KafkaProducer
import json
import time

# Initialize Kafka Consumers for OHLCV and Sentiment
ohlcv_consumer = KafkaConsumer(
    'ohlcv_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

sentiment_consumer = KafkaConsumer(
    'sentiment_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

# Initialize Kafka Producer to publish trade signals
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Trade Signal Kafka topic
trade_signal_topic = 'trade_signals'

# Simple in-memory storage
ohlcv_data = {}
sentiment_data = []

def process_sentiment(sentiment):
    # Only act if sentiment is strong
    score = sentiment['sentiment_score']
    symbol = extract_symbol_from_title(sentiment['title'])

    if symbol:
        action = None
        if score > 0.3:
            action = 'BUY'
        elif score < -0.3:
            action = 'SELL'

        if action:
            trade_signal = {
                "symbol": symbol,
                "action": action,
                "confidence": round(abs(score), 2),
                "timestamp": sentiment['timestamp'],
                "reason": sentiment['title']
            }
            producer.send(trade_signal_topic, value=trade_signal)
            print(f"Sent Trade Signal: {trade_signal}")

def extract_symbol_from_title(title: str):
    # Very basic mapping based on company names appearing in title
    if "Tesla" in title or "TSLA" in title:
        return "TSLA"
    elif "Apple" in title or "AAPL" in title:
        return "AAPL"
    elif "Microsoft" in title or "MSFT" in title:
        return "MSFT"
    elif "Reddit" in title or "RDDT" in title:
        return "RDDT"
    else:
        return None

if __name__ == "__main__":
    print("⚡ Trading model running...")

    # Simple loop to poll both streams
    while True:
        # Check for new sentiment
        for sentiment_msg in sentiment_consumer.poll(timeout_ms=500).values():
            for record in sentiment_msg:
                sentiment = record.value
                process_sentiment(sentiment)

        # You can also process OHLCV data if needed
        # For now, we react only to sentiment
        time.sleep(1)
