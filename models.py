
from datetime import datetime
from sqlmodel import SQLModel, Field


class MetricPoint(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    service: str = Field(index=True)

    metric: str = Field(index=True)

    timestamp: datetime = Field(index=True)

    value: float
