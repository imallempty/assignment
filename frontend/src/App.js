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

  useEffect(() => {
    let ws;
    let reconnectTimer;

    const connect = () => {
      ws = new WebSocket('ws://localhost:8000/ws');
      wsRef.current = ws;

      ws.onopen = () => {
        ws.send(JSON.stringify({ timeRange }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setStats(prev => {
          // 값이 같으면 업데이트 안 함
          if (
            prev.total === data.total &&
            prev.overall_avg_speed === data.overall_avg_speed &&
            JSON.stringify(prev.type_stats) === JSON.stringify(data.type_stats)
          ) {
            return prev;
          }
          return data;
        });
      };

      ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
      };

      ws.onclose = () => {
        reconnectTimer = setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, []);

  useEffect(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ timeRange }));
    }
  }, [timeRange]);

  const TYPE_COLORS = {
    Pedestrian: '#4ade80',
    Bike: '#60a5fa',
    Vehicle: '#f97316',
    LargeVehicle: '#a78bfa',
  };

  const isEmpty = stats.total === 0;

  return (
    <div className="app">
      <header className="header">
        <h1>교통 모니터링 대시보드</h1>
        <select
          className="select"
          value={timeRange}
          onChange={(e) => setTimeRange(Number(e.target.value))}
        >
          <option value={5}>최근 5분</option>
          <option value={30}>최근 30분</option>
        </select>
      </header>

      <main className="main">
        <div className="kpi-grid">
          <div className="kpi-card">
            <span className="kpi-label">총 감지 수</span>
            {isEmpty
              ? <span className="empty">데이터 없음</span>
              : <span className="kpi-num">{stats.total.toLocaleString()}</span>
            }
          </div>
          <div className="kpi-card">
            <span className="kpi-label">평균 속도</span>
            {isEmpty
              ? <span className="empty">데이터 없음</span>
              : <span className="kpi-num">{stats.overall_avg_speed.toFixed(1)}<small> m/s</small></span>
            }
          </div>
        </div>

        <section className="section">
          <h2 className="section-title">타입별 현황</h2>
          {isEmpty ? (
            <div className="empty-box">데이터 없음</div>
          ) : (
            <div className="type-grid">
              {stats.type_stats.map((item) => (
                <div className="type-card" key={item.type}>
                  <div
                    className="type-dot"
                    style={{ background: TYPE_COLORS[item.type] ?? '#94a3b8' }}
                  />
                  <span className="type-name">{item.type}</span>
                  <span className="type-count">{item.count}개</span>
                  <span className="type-speed">{item.avg_speed.toFixed(1)} m/s</span>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
} 

export default App;