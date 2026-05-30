import GameCanvas from "./GameCanvas";
// import GameOverlay from "./GameOverlay";
import "./GameStage.css";

export default function GameStage() {
  // const isGameActive = false;

  return (
    <main className="game-stage">
      <div className="game-box">
        <GameCanvas />
        {/* {!isGameActive && <GameOverlay />} */}
      </div>
    </main>
  );
}
