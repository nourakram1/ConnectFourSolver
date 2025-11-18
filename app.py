from flask import Flask, request, jsonify

from Board import Board
from Solver import Solver

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    # Expecting data: { "player": [...], "free_positions": [...] }
    player = bytearray(data.get("player", []))
    free_positions = bytearray(data.get("free_positions", []))

    board = Board(player, free_positions)
    next_move = Solver.solve(board)

    if next_move is None:
        return jsonify({"status": "terminal", "next_board": None})

    return jsonify({
        "status": "ok",
        "next_board": {
            "player": list(next_move.player),
            "free_positions": list(next_move.free_positions)
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
