from pydantic import BaseModel
from typing import List
from datetime import datetime


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
    
class TypeInfo(BaseModel):
    type: str
    count: int
    avg_speed: float

class Stats(BaseModel):
    total: int
    type_stats: List[TypeInfo]
    overall_avg_speed: float