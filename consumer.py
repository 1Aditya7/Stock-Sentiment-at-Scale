# consumer.py
from kafka import KafkaConsumer
import json

# Connect to the local Kafka broker
consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Continuously listen for messages
for message in consumer:
    print(f"Received: {message.value}")
