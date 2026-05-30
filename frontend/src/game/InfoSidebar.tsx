import PlayerStats from "./PlayerStats";
import ControlsGuide from "./ControlsGuide";
import "./InfoSidebar.css";

export default function InfoSidebar() {
  return (
    <div className="score-panel">
      <h2>Score</h2>
      <PlayerStats />
      <ControlsGuide />
    </div>
  );
}
