// frontend/src/App.js
import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [stats, setStats] = useState({
    total: 0,
    type_stats: [],
    overall_avg_speed: 0
  });
  const [timeRange, setTimeRange] = useState(5);
  const wsRef = useRef(null);

  // WebSocket 연결 및 시간 범위 전송
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;
    
    ws.onopen = () => {
      console.log('WebSocket Connected');
      // 연결 즉시 시간 범위 전송
      ws.send(JSON.stringify({ timeRange: timeRange }));
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStats(data);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket Disconnected');
    };
    
    return () => ws.close();
  }, []);

  // 시간 범위 변경 시 WebSocket으로 전송
  useEffect(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ timeRange: timeRange }));
      console.log(`Sent timeRange: ${timeRange} minutes`);
    }
  }, [timeRange]);

  return (
    <div className="App">
      <header className="dashboard-header">
        <h1>실시간 교통 모니터링 대시보드</h1>
      </header>

      {/* 시간 범위 선택 */}
      <div className="time-selector">
        <label>시간 범위: </label>
        <select 
          value={timeRange} 
          onChange={(e) => setTimeRange(Number(e.target.value))}
        >
          <option value={5}>최근 5분</option>
          <option value={30}>최근 30분</option>
        </select>
      </div>

      {/* KPI 카드 */}
      <div className="kpi-container">
        <div className="kpi-card">
          <h3>총 감지 수</h3>
          <p className="kpi-value">{stats.total}</p>
        </div>

        <div className="kpi-card">
          <h3>평균 속도</h3>
          <p className="kpi-value">{stats.overall_avg_speed.toFixed(2)} m/s</p>
        </div>
      </div>

      {/* 타입별 감지 수 */}
      <div className="type-stats">
        <h2>타입별 감지 현황</h2>
        {stats.type_stats.length === 0 ? (
          <p className="no-data">데이터 없음</p>
        ) : (
          <div className="type-list">
            {stats.type_stats.map((type, index) => (
              <div key={index} className="type-item">
                <span className="type-name">{type.type}</span>
                <span className="type-count">{type.count}개</span>
                <span className="type-speed">{type.avg_speed.toFixed(2)} m/s</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;