const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const grid = 16;

let state = null;
let count = 0;
let gameStarted = false;

let direction = "RIGHT";

function loop() {
    requestAnimationFrame(loop);
    if (++count < 4) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!gameStarted) {
        ctx.fillStyle = "white";
        ctx.font = "20px monospace";
        ctx.textAlign = "center";
        ctx.fillText("Press arrow key to start", canvas.width/2, canvas.height/2);
        return;
    }

    if (!state) return;
    count = 0;

    if (state.type === "gameover") {
        ctx.fillStyle = "red";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "white";
        ctx.font = "20px monospace";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width/2, canvas.height/2 - 20);
        ctx.fillText("Score: " + state.points, canvas.width/2, canvas.height/2 + 10);
        ctx.fillText("Press r to restart", canvas.width/2, canvas.height/2 + 40);

        if (state.new_highscore) {
            ctx.fillText("CONGRATULATIONS!", canvas.width/2, canvas.height/2 + 100);
            ctx.fillText("YOU REACHED A NEW HIGH SCORE!", canvas.width/2, canvas.height/2 + 130);
    }
        return;
    }

    ctx.fillStyle = "red";
    ctx.fillRect(state.food[0], state.food[1], grid-1, grid-1);

    const player = state.player;

    ctx.fillStyle = "green";
    player.position.forEach(cell => {
        ctx.fillRect(cell[0], cell[1], grid-1, grid-1);
    });
}

document.addEventListener('keydown', e => {
    let moved = false;

    if (e.key === "r" || e.key === "R") {
        resetGame();
        return;
    }

    switch(e.key) {
        case "ArrowUp": direction = "UP"; moved = true; break;
        case "ArrowDown": direction = "DOWN"; moved = true; break;
        case "ArrowLeft": direction = "LEFT"; moved = true; break;
        case "ArrowRight": direction = "RIGHT"; moved = true; break;
    }

    if (moved && !gameStarted) {
        gameStarted = true;
        sendMove();
    }
});

function resetGame() {
    fetch("http://127.0.0.1:5000/reset", {
        method: "POST"
    })
    .then(() => {
        state = null;
        gameStarted = false;
        direction = "RIGHT";
    })
    .catch(err => console.error("Reset error:", err));
}

function sendMove() {
    fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            player: 0,
            direction: direction
        })
    })
    .then(res => res.json())
    .then(data => state = data)
    .catch(err => console.error("Error:", err));
}

setInterval(() => {
    if (!gameStarted) return;
    sendMove();
}, 120);

requestAnimationFrame(loop);