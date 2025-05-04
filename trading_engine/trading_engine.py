import os
import json
import time
from kafka import KafkaConsumer

# Load Kafka broker from environment variable
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TRADE_SIGNAL_TOPIC = "trade_signals"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    TRADE_SIGNAL_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="trading-engine-group"
)

# In-memory portfolio state
portfolio = {}
cash_balance = 100000  # Initial cash in USD

# Mock stock prices
mock_price_per_stock = {
    "TSLA": 250,
    "AAPL": 180,
    "MSFT": 400,
    "RDDT": 50
}

def execute_trade(signal):
    global cash_balance
    symbol = signal.get("symbol")
    action = signal.get("action")
    confidence = signal.get("confidence", 0)
    price = mock_price_per_stock.get(symbol, 100)
    qty = int(confidence * 10)
    cost = qty * price

    print(f"\n📩 Received signal: {signal}")

    if action == "BUY":
        if cash_balance >= cost:
            portfolio[symbol] = portfolio.get(symbol, 0) + qty
            cash_balance -= cost
            print(f"🟢 Bought {qty} shares of {symbol} @ ${price} | 💰 Cash: ${cash_balance:.2f}")
        else:
            print(f"❌ Not enough cash to BUY {symbol}. Required: ${cost}, Available: ${cash_balance}")
    elif action == "SELL":
        if portfolio.get(symbol, 0) >= qty:
            portfolio[symbol] -= qty
            cash_balance += cost
            print(f"🔴 Sold {qty} shares of {symbol} @ ${price} | 💰 Cash: ${cash_balance:.2f}")
        else:
            print(f"❌ Not enough shares to SELL {symbol}. Holding: {portfolio.get(symbol, 0)}")

    print(f"📊 Portfolio: {portfolio} | Cash: ${cash_balance:.2f}")

if __name__ == "__main__":
    print("🏦 Trading Engine Running...")

    try:
        while True:
            raw_messages = consumer.poll(timeout_ms=500)
            for _, records in raw_messages.items():
                for record in records:
                    execute_trade(record.value)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Trading engine stopped.")
    except Exception as e:
        print(f"❗ Error: {e}")
