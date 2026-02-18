# backend/routers/ingest.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(tags=["ingest"])

@router.post("/ingest")
def ingest_data(event_data: schemas.IngestEvent, db: Session = Depends(get_db)):
    result = crud.create_event(db, event_data)
    return {"status": "success", "event_id": result.id}