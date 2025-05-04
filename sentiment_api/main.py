from fastapi import FastAPI, Response
from sentiment_api.signals import get_signals, add_signal
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Prometheus metric
request_count = Counter("api_requests_total", "Total API Requests", ["endpoint"])

@app.get("/signals")
def signals():
    request_count.labels(endpoint="/signals").inc()
    return get_signals()

@app.post("/add_signal")
def post_signal(symbol: str, sentiment: str):
    request_count.labels(endpoint="/add_signal").inc()
    add_signal(symbol, sentiment)
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
