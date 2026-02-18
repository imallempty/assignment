# backend/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import asyncio
import json
import crud
from database import SessionLocal

router = APIRouter(tags=["websocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    time_range = 5  # 기본값 5분
    
    try:
        while True:
            # 클라이언트로부터 메시지 받기 (non-blocking)
            try:
                message = await asyncio.wait_for(
                    websocket.receive_text(), 
                    timeout=0.1
                )
                data = json.loads(message)
                if 'timeRange' in data:
                    time_range = data['timeRange']
                    print(f"Time range updated to: {time_range} minutes")
            except asyncio.TimeoutError:
                pass  # 메시지 없으면 계속 진행
            
            # 통계 계산
            db = SessionLocal()
            to_time = datetime.now(timezone.utc)
            from_time = to_time - timedelta(minutes=time_range)
            
            stats = crud.get_stats(db, from_time, to_time, zone=None)
            db.close()
            
            # 클라이언트로 전송
            await websocket.send_json(stats)
            
            # 2초 대기
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        print("Client disconnected")