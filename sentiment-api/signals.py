from typing import List
from datetime import datetime

signals = []

def add_signal(symbol: str, sentiment: str):
    signals.append({
        "symbol": symbol,
        "sentiment": sentiment,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_signals() -> List[dict]:
    return signals[-50:]  # last 50 signals
