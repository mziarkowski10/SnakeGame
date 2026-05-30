import "./Sidebar.css";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>SNAKE GAME</h1>
      </div>
      <StatsSection />
      <ControlsSection />
    </aside>
  );
}

function StatsSection() {
  return (
    <div className="sidebar-section">
      <h3>STATS</h3>
      <div className="stat-item">
        <span className="stat-label">Score:</span>
        <span className="stat-value">0000</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">High Score:</span>
        <span className="stat-value">1500</span>
      </div>
    </div>
  );
}

function ControlsSection() {
  return (
    <div className="sidebar-section">
      <h3>CONTROLS</h3>
      <div className="stat-item">
        <span>Move:</span>
        <span>W, A, S, D</span>
      </div>
    </div>
  );
}
