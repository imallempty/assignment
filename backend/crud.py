from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import func
from datetime import datetime


def create_event(db: Session, event_data: schemas.IngestEvent):
    db_event = models.Event(
        timestamp=event_data.timestamp,
        zone=event_data.zone
    )
    db.add(db_event)
    db.flush() 
    
    for obj in event_data.objects:
        db_obj = models.Object(
            event_id=db_event.id,
            uuid=obj.uuid,
            type=obj.type,
            x=obj.x,
            y=obj.y,
            speed_ms=obj.speed_ms
        )
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_event)
    return db_event


def get_stats(db: Session, from_time: datetime, to_time: datetime, zone: str = None):
    query = db.query(models.Object).join(models.Event)
    
    query = query.filter(models.Event.timestamp >= from_time)
    query = query.filter(models.Event.timestamp <= to_time)
    
    if zone:
        query = query.filter(models.Event.zone == zone)
    
    all_objects = query.all()
    
    if not all_objects:
        return {
            "total": 0,
            "type_stats": [],
            "overall_avg_speed": 0.0
        }
    
    total_objects = len(all_objects)
    
    overall_avg_speed = sum(obj.speed_ms for obj in all_objects) / total_objects
    
    type_dict = {}
    for obj in all_objects:
        if obj.type not in type_dict:
            type_dict[obj.type] = {"speeds": [], "count": 0}
        type_dict[obj.type]["speeds"].append(obj.speed_ms)
        type_dict[obj.type]["count"] += 1
    
    type_stats = [
        {
            "type": t,
            "count": data["count"],
            "avg_speed": sum(data["speeds"]) / len(data["speeds"])
        }
        for t, data in type_dict.items()
    ]
    
    return {
        "total": total_objects,
        "type_stats": type_stats,
        "overall_avg_speed": overall_avg_speed,
    }