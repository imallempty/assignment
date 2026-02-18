# backend/routers/stats.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import schemas, crud
from database import get_db

router = APIRouter(tags=["stats"])

@router.get("/stats", response_model=schemas.Stats)
def get_stats(
    from_time: datetime = Query(..., alias="from"),  
    to_time: datetime = Query(..., alias="to"),      
    zone: Optional[str] = Query(None),               
    db: Session = Depends(get_db)
):
    result = crud.get_stats(db, from_time, to_time, zone)
    return result