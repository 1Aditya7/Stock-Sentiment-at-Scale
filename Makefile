.PHONY: up kafka-topics news sentiment trade api dash all

up:
	docker compose up -d --build

kafka-topics:
	docker exec stock-sentiment-at-scale-kafka-1 bash -c "/usr/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sentiment_data || true"
	docker exec stock-sentiment-at-scale-kafka-1 bash -c "/usr/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic trade_signals || true"

news:
	python news_producer/news_producer.py

sentiment:
	python sentiment_analyzer/sentiment_analyzer.py

trade:
	python trading_model/trading_model.py

api:
	uvicorn sentiment_api.main:app --reload --port 8000

dash:
	cd dashboard && npm run dev

all: up kafka-topics
	@echo "🟢 Environment ready. Run each stage via: make news, make sentiment, make trade, make api, make dash"

.PHONY: stop

stop:
	@echo "🔴 Stopping FastAPI, Kafka, Zookeeper, and Dashboard..."
	-@pkill -f uvicorn || true
	-@pkill -f next || true
	-@docker compose down -v || true
