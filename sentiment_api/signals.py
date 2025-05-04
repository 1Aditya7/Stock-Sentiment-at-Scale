from typing import List
from trading_model import get_latest_signals
from datetime import datetime

signals = []

def add_signal(symbol: str, sentiment: str):
    signals.append({
        "symbol": symbol,
        "sentiment": sentiment,
        "timestamp": datetime.utcnow().isoformat()
    })


def get_signals():
    return get_latest_signals()
