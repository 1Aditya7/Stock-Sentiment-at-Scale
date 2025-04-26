# producer.py
from kafka import KafkaProducer
import json
import time

# Connect to the local Kafka broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'test_topic'  # You can choose any name

# Send 10 simple messages
for i in range(10):
    message = {"number": i}
    producer.send(topic, value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
