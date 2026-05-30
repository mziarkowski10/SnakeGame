import "./GameCanvas.css";
import { useEffect, useRef } from "react";

const BASE_URL = "http://localhost:5000";
const grid = 16;

export default function GameCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const stateRef = useRef<any>(null);
  const directionRef = useRef<string>("RIGHT");
  const gameStartedRef = useRef(false);
  const countRef = useRef(0);

  // Handle keyboard input
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      let moved = false;

      if (e.key === "r" || e.key === "R") {
        resetGame();
        return;
      }

      switch (e.key) {
        case "ArrowUp":
          directionRef.current = "UP";
          moved = true;
          break;
        case "ArrowDown":
          directionRef.current = "DOWN";
          moved = true;
          break;
        case "ArrowLeft":
          directionRef.current = "LEFT";
          moved = true;
          break;
        case "ArrowRight":
          directionRef.current = "RIGHT";
          moved = true;
          break;
      }

      if (moved && !gameStartedRef.current) {
        gameStartedRef.current = true;
        sendMove();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Polling loop
  useEffect(() => {
    const pollInterval = setInterval(() => {
      if (!gameStartedRef.current) return;
      sendMove();
    }, 120);

    return () => clearInterval(pollInterval);
  }, []);

  // Render loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const loop = () => {
      requestAnimationFrame(loop);
      if (++countRef.current < 4) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!gameStartedRef.current) {
        ctx.fillStyle = "white";
        ctx.font = "20px monospace";
        ctx.textAlign = "center";
        ctx.fillText(
          "Press arrow key to start",
          canvas.width / 2,
          canvas.height / 2,
        );
        return;
      }

      if (!stateRef.current) return;

      countRef.current = 0;

      // Draw food
      ctx.fillStyle = "red";
      ctx.fillRect(
        stateRef.current.food[0],
        stateRef.current.food[1],
        grid - 1,
        grid - 1,
      );

      // Draw player
      ctx.fillStyle = "green";
      stateRef.current.player.position.forEach((cell: number[]) => {
        ctx.fillRect(cell[0], cell[1], grid - 1, grid - 1);
      });
    };

    loop();
  }, []);

  async function sendMove() {
    try {
      const response = await fetch(`${BASE_URL}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player: 0,
          direction: directionRef.current,
        }),
      });
      const data = await response.json();
      stateRef.current = data;
    } catch (err) {
      console.error("Error:", err);
    }
  }

  async function resetGame() {
    try {
      await fetch(`${BASE_URL}/reset`, {
        method: "POST",
      });
      stateRef.current = null;
      gameStartedRef.current = false;
      directionRef.current = "RIGHT";
    } catch (err) {
      console.error("Reset error:", err);
    }
  }

  return (
    <canvas
      className="game-canvas"
      ref={canvasRef}
      id="stage-canvas"
      width={400}
      height={400}
    >
      Your browser does not support graphics.
    </canvas>
  );
}
