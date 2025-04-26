# sentiment_analyzer.py
from kafka import KafkaConsumer, KafkaProducer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Initialize Kafka Consumer and Producer
consumer = KafkaConsumer(
    'news_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'  # Start reading from the beginning if no committed offset
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# New Kafka topic to publish sentiment scores
sentiment_topic = 'sentiment_data'

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

for message in consumer:
    news = message.value
    title = news.get('title', '')

    sentiment_scores = analyzer.polarity_scores(title)
    compound_score = sentiment_scores['compound']

    # Label based on compound score
    if compound_score >= 0.05:
        sentiment_label = 'positive'
    elif compound_score <= -0.05:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'

    sentiment_message = {
        "source": news.get('source', ''),
        "title": title,
        "link": news.get('link', ''),
        "timestamp": news.get('timestamp', ''),
        "sentiment": sentiment_label,
        "sentiment_score": compound_score
    }

    producer.send(sentiment_topic, value=sentiment_message)
    print(f"Sent Sentiment: {sentiment_message}")
