from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime, timezone


class IngestObject(BaseModel):
    uuid: str
    type: str
    x: float
    y: float
    speed_ms: float


class IngestEvent(BaseModel):
    timestamp: datetime
    zone: str
    objects: List[IngestObject]

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class TypeInfo(BaseModel):
    type: str
    count: int
    avg_speed: float


class Stats(BaseModel):
    total: int
    type_stats: List[TypeInfo]