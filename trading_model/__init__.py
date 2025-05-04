from .trading_model import get_latest_signals
import os
import json
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TRADE_SIGNAL_TOPIC = "trade_signals"

def get_latest_signals(limit=20):
    consumer = KafkaConsumer(
        TRADE_SIGNAL_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='latest',
        enable_auto_commit=False,
        group_id=None,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Pull latest N messages
    messages = []
    try:
        records = consumer.poll(timeout_ms=2000, max_records=limit)
        for tp_records in records.values():
            for record in tp_records:
                messages.append(record.value)
    finally:
        consumer.close()

    return messages
