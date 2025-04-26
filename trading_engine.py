# trading_engine.py
from kafka import KafkaConsumer
import json
import time

# Initialize Kafka Consumer for trade signals
consumer = KafkaConsumer(
    'trade_signals',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

# Simple mock portfolio
portfolio = {}
cash_balance = 100000  # Starting cash ($100,000)

# Simple assumptions
mock_price_per_stock = {
    "TSLA": 250,
    "AAPL": 180,
    "MSFT": 400,
    "RDDT": 50
}

def execute_trade(signal):
    global cash_balance
    symbol = signal['symbol']
    action = signal['action']
    confidence = signal['confidence']
    timestamp = signal['timestamp']
    reason = signal['reason']

    # Assume fixed price (mock) for simplicity
    price = mock_price_per_stock.get(symbol, 100)

    qty = int(confidence * 10)  # Trade size proportional to confidence
    cost = qty * price

    if action == "BUY":
        if cash_balance >= cost:
            portfolio[symbol] = portfolio.get(symbol, 0) + qty
            cash_balance -= cost
            print(f"🟢 Bought {qty} shares of {symbol} at ${price} each | New cash: ${cash_balance:.2f}")
        else:
            print(f"❌ Insufficient cash to buy {symbol}. Skipping.")
    elif action == "SELL":
        if portfolio.get(symbol, 0) >= qty:
            portfolio[symbol] -= qty
            cash_balance += cost
            print(f"🔴 Sold {qty} shares of {symbol} at ${price} each | New cash: ${cash_balance:.2f}")
        else:
            print(f"❌ Insufficient shares to sell {symbol}. Skipping.")

    print(f"📈 Portfolio Now: {portfolio} | Cash: ${cash_balance:.2f}")

if __name__ == "__main__":
    print("🏦 Trading Engine Running...")

    while True:
        for msg in consumer.poll(timeout_ms=500).values():
            for record in msg:
                trade_signal = record.value
                execute_trade(trade_signal)
        time.sleep(1)
