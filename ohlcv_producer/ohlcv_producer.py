# ohlcv_producer.py
from kafka import KafkaProducer
import yfinance as yf
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'ohlcv_data'

# Stock symbols you want to track
symbols = ['AAPL', 'MSFT', 'TSLA']

while True:
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')
        
        if not data.empty:
            latest = data.iloc[-1]
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
            print(f"Sent OHLCV: {message}")
    
    time.sleep(60)  # Wait 1 minute before fetching again
