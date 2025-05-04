import os
import json
import time
from kafka import KafkaConsumer, KafkaProducer
import requests

# Kafka setup from environment
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TRADE_SIGNAL_TOPIC = "trade_signals"

# Global in-memory store
latest_signals = []

# Kafka Consumers
sentiment_consumer = KafkaConsumer(
    "sentiment_data",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="sentiment-consumer-group"
)

ohlcv_consumer = KafkaConsumer(
    "ohlcv_data",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="ohlcv-consumer-group"
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def extract_symbol_from_title(title: str):
    title = title.upper()
    if "TESLA" in title or "TSLA" in title:
        return "TSLA"
    elif "APPLE" in title or "AAPL" in title:
        return "AAPL"
    elif "MICROSOFT" in title or "MSFT" in title:
        return "MSFT"
    elif "REDDIT" in title or "RDDT" in title:
        return "RDDT"
    return None

def process_sentiment(sentiment: dict):
    score = sentiment.get("sentiment_score", 0)
    symbol = extract_symbol_from_title(sentiment.get("title", ""))

    if not symbol:
        return

    action = "BUY" if score > 0.3 else "SELL" if score < -0.3 else None

    if action:
        trade_signal = {
            "symbol": symbol,
            "action": action,
            "confidence": round(abs(score), 2),
            "timestamp": sentiment.get("timestamp", ""),
            "reason": sentiment.get("title", "")
        }
        producer.send(TRADE_SIGNAL_TOPIC, value=trade_signal)
        send_to_api(symbol, action.lower())
        latest_signals.append(trade_signal)
        print(f"📤 Sent Trade Signal: {trade_signal}")

def get_latest_signals():
    return latest_signals[-50:]

def main_loop():
    print("⚡ Trading Model Running...")
    try:
        while True:
            # Process sentiment data
            sentiment_batches = sentiment_consumer.poll(timeout_ms=500)
            for records in sentiment_batches.values():
                for record in records:
                    process_sentiment(record.value)

            # Placeholder: future OHLCV logic goes here
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Trading model stopped by user.")
    except Exception as e:
        print(f"❌ Error in trading model: {e}")
        
def send_to_api(symbol, sentiment):
    try:
        requests.post("http://localhost:8000/add_signal", params={"symbol": symbol, "sentiment": sentiment})
    except Exception as e:
        print(f"❌ Failed to send signal to API: {e}")

if __name__ == "__main__":
    main_loop()
