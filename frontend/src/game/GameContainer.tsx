import GameViewport from "./GameViewport";
import InfoSidebar from "./InfoSidebar";
import "./GameContainer.css";

export default function GameContainer() {
  return (
    <div className="game-container">
      <GameViewport />
      <InfoSidebar />
    </div>
  );
}
