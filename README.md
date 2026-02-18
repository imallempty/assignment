## 실행 방법
### Docker Compose로 전체 실행
docker-compose up --build

# 접속
# - Backend API: http://localhost:8000/docs
# - Frontend Dashboard: http://localhost:3000

## API 사용 예시

### 1. 데이터 수신 (POST /ingest)

**curl 예시:**
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2026-02-17T06:30:00Z",
    "zone": "A구역",
    "objects": [
      {"uuid": "abc-123", "type": "Pedestrian", "x": 12.5, "y": 3.2, "speed_ms": 1.2},
      {"uuid": "def-456", "type": "Vehicle", "x": 45.1, "y": 8.7, "speed_ms": 8.3}
    ]
  }'
```

**응답:**
```json
{
  "status": "success",
  "event_id": 1
}
```

### 2. 통계 조회 (GET /stats)

**curl 예시:**
```bash
curl -X GET "http://localhost:8000/stats?from=2026-02-17T06:00:00Z&to=2026-02-17T07:00:00Z&zone=A구역"
```

**응답:**
```json
{
  "total": 4,
  "type_stats": [
    {
      "type": "Pedestrian",
      "count": 2,
      "avg_speed": 1.25
    },
    {
      "type": "Vehicle",
      "count": 2,
      "avg_speed": 8.3
    }
  ],
  "overall_avg_speed": 4.775
}
```

### 3. WebSocket 연결
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({ timeRange: 5 }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

## 간단 아키텍처 설명
![alt text](image.png)

**데이터 흐름:**
1. POST /ingest → Event + Objects DB 저장
2. WebSocket → 2초마다 최신 통계 계산 및 전송
3. React Dashboard → 실시간 KPI 자동 갱신