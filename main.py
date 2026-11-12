
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from datetime import datetime, timezone

from database import engine
from models import MetricPoint

app = FastAPI(
    title="Metrics Insight API",
    description="API for application metrics monitoring",
    version="1.0.0"
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def home():
    return {
        "message": "Welcome to Metrics Insight API",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {"status": "Healthy"}


@app.post("/metrics")
def create_metric(metric: MetricPoint, session: Session = Depends(get_session)):

    timestamp = datetime.fromisoformat(
        str(metric.timestamp).replace("Z", "+00:00")
    )

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    metric.timestamp = timestamp
    metric.id = None

    session.add(metric)
    session.commit()
    session.refresh(metric)

    return {
        "message": "Metric saved successfully",
        "data": metric
    }


@app.get("/metrics")
def get_metrics(session: Session = Depends(get_session)):

    statement = select(MetricPoint)
    results = session.exec(statement).all()

    return {
        "total_records": len(results),
        "data": results
    }
