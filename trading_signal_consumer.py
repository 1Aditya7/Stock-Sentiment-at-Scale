# trade_signal_consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'trade_signals',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

for message in consumer:
    print(message.value)
