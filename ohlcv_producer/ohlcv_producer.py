import os
import json
import time
import yfinance as yf
from kafka import KafkaProducer

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SYMBOL_LIST = os.getenv("SYMBOLS", "AAPL,MSFT,TSLA").split(',')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = 'ohlcv_data'

def fetch_and_send_ohlcv():
    for symbol in SYMBOL_LIST:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')

            if data.empty:
                print(f"⚠️ No data for {symbol}")
                continue

            latest = data.iloc[-1]
            if latest.isnull().any():
                print(f"⚠️ Incomplete data for {symbol}")
                continue

            message = {
                "symbol": symbol,
                "timestamp": str(latest.name),
                "open": float(latest['Open']),
                "high": float(latest['High']),
                "low": float(latest['Low']),
                "close": float(latest['Close']),
                "volume": int(latest['Volume'])
            }

            producer.send(topic, value=message)
            print(f"📤 Sent OHLCV: {message}")

        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_send_ohlcv()
        print("✅ Fetched and sent OHLCV batch.")
        time.sleep(60)
