Stage 1 — The Single-Player MVP (3 Routes)
This streamlined version bypasses lobby lists and join handshakes. Creating a game instantly provisions a player slot and starts the internal simulation loop.

1. Game Provisioning
   HTTP Method & URI: POST /api/v1/games

Status Code: 201 Created

Request Payload:

JSON
{
"board_width": 20,
"board_height": 20
}

Response Payload:

JSON
{
"game_id": "g_mvp_777",
"player_id": "p_solo_1",
"secret_token": "tok_mvp_secure_string_abc123",
"status": "active"
}

2. Directional Input Buffer Pipeline
   HTTP Method & URI: POST /api/v1/games/{gameId}/inputs

Headers Required: Authorization: Bearer tok_mvp_secure_string_abc123

Status Code: 202 Accepted

Request Payload:

JSON
{
"direction": "RIGHT" // Supported enums: UP, DOWN, LEFT, RIGHT
}

Response Payload:

JSON
{
"status": "buffered"
}

3. State Synchronization (Long-Polling Engine)
   HTTP Method & URI: GET /api/v1/games/{gameId}/state

Query Parameters: ?since_tick=104

Status Code: 200 OK

Response Payload:

JSON
{
"game_id": "g_mvp_777",
"status": "active",
"current_tick": 105,
"players": [
{
"player_id": "p_solo_1",
"alive": true,
"score": 3,
"segments": [[10, 5], [9, 5], [8, 5]]
}
],
"food": [[4, 12]]
}

Part 2: Stage 2 — The Multiplayer Target Architecture (7 Routes)
This decouples match creation from joining, introduces lobby discovery, and uses a polymorphic array so that up to 4 players can share the board using identical gameplay routes.

1. Match Discovery & Lifecycle
   POST /api/v1/games (Creates empty lobby)

Status: 201 Created

Payload: {"max_players": 4, "board_width": 20, "board_height": 20}

Response: {"game_id": "g_multi_101", "status": "waiting"}

GET /api/v1/games (Lobby Browser List)

Status: 200 OK

Response: [{"game_id": "g_multi_101", "status": "waiting", "current_players": 1, "max_players": 4}]

GET /api/v1/games/{gameId} (Fetch static map metadata)

Status: 200 OK

Response: {"game_id": "g_multi_101", "board_width": 20, "board_height": 20, "max_players": 4}

DELETE /api/v1/games/{gameId} (Admin/System Teardown)

Status: 204 No Content

2. Player Session Handshakes
   POST /api/v1/games/{gameId}/players (Join Lobby)

Status: 201 Created

Payload: {"player_name": "Pythonista"}

Response: {"player_id": "p_multi_99", "secret_token": "tok_multi_xyz_789"}

DELETE /api/v1/games/{gameId}/players/{playerId} (Leave/Disconnect)

Status: 204 No Content (Requires Auth Header)

3. Real-Time Flow Streams
   POST /api/v1/games/{gameId}/inputs — Identical contract to Stage 1.

GET /api/v1/games/{gameId}/state — Identical schema structure to Stage 1, but the players array seamlessly grows with multiple active entities:

JSON
{
"game_id": "g_multi_101",
"status": "active",
"current_tick": 482,
"players": [
{ "player_id": "p_multi_99", "alive": true, "score": 12, "segments": [[14, 2], [14, 3]] },
{ "player_id": "p_multi_88", "alive": true, "score": 4, "segments": [[2, 10], [2, 11]] }
],
"food": [[5, 5], [19, 11]]
}
