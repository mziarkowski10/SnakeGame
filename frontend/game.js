const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const grid = 16;
let state = null;
let count = 0;

function loop() {
    requestAnimationFrame(loop);
    if (++count < 4) return;
    if (!state) return;
    count = 0;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (state.type === "gameover") {
        ctx.fillStyle = "red";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        return;
    }

    ctx.fillStyle = "red";
    ctx.fillRect(state.food[0], state.food[1], grid-1, grid-1);

    const colors = ["green", "blue"];
    state.players.forEach(player => {
        ctx.fillStyle = colors[player.player] || "white";
        player.snake.forEach(cell => {
            ctx.fillRect(cell[0], cell[1], grid-1, grid-1);
        });
    });
}

document.addEventListener('keydown', e => {
    let move = null;
    let player = null;

    switch(e.key) {
        case "ArrowUp": move="UP"; player=0; break;
        case "ArrowDown": move="DOWN"; player=0; break;
        case "ArrowLeft": move="LEFT"; player=0; break;
        case "ArrowRight": move="RIGHT"; player=0; break;
        case "w": move="UP"; player=1; break;
        case "s": move="DOWN"; player=1; break;
        case "a": move="LEFT"; player=1; break;
        case "d": move="RIGHT"; player=1; break;
    }

    if(move !== null) sendMove(move, player);
});

function sendMove(direction, player) {
    fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({player: player, direction: direction})
    })
    .then(res => res.json())
    .then(data => state = data)
    .catch(err => console.error("Error:", err));
}

requestAnimationFrame(loop);