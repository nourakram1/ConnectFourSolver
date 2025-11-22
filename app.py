from flask import Flask, request, jsonify
from app.Solver import Solver
from app.Board import Board
from util.SchemaValidator import SchemaValidator

app = Flask(__name__)

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()

    is_valid, err, validated_data = SchemaValidator.validate(data)
    if not is_valid:
        return jsonify({"error": err}), 400

    board_data = validated_data["board"]
    algorithm = validated_data["algorithm"]
    depth = validated_data["depth"]
    prune = validated_data["prune"]
    ai_player = validated_data["ai_player"]

    board = Board(matrix=board_data)

    solver = Solver(depth=depth, prune=prune, ai_player=ai_player)

    if algorithm == "minimax":
        best_col, best_val, nodes, root = solver.run_minimax(board)
    elif algorithm == "expectiminimax":
        best_col, best_val, nodes, root = solver.run_expectiminimax(board)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({
        "algorithm": algorithm,
        "best_col": best_col,
        "value": best_val,
        "nodes_expanded": nodes,
        "tree": root.to_json()
    })

if __name__ == "__main__":
    app.run(debug=True)
