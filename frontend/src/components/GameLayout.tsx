import Sidebar from "./Sidebar";
import GameStage from "./GameStage";
import "./GameLayout.css";

export default function GameLayout() {
  return (
    <div className="game-layout">
      <GameStage />
      <Sidebar />
    </div>
  );
}
