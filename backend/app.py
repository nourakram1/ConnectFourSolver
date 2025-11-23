from flask import Flask, request, jsonify
from flask_cors import CORS
from app.Solver import Solver
from app.Board import Board
from util.SchemaValidator import SchemaValidator

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()

    # Debug: print received data
    print("Received data:")
    print(f"Board: {data.get('board')}")
    print(f"Algorithm: {data.get('algorithm')}")

    is_valid, err, validated_data = SchemaValidator.validate(data)
    if not is_valid:
        return jsonify({"error": err}), 400

    board_data = validated_data["board"]
    algorithm = validated_data["algorithm"]
    depth = validated_data["depth"]
    prune = validated_data["prune"]
    ai_player = validated_data["ai_player"]

    try:
        board = Board(matrix=board_data)
    except ValueError as e:
        print(f"Board validation error: {e}")
        return jsonify({"error": str(e)}), 400

    solver = Solver(depth=depth, prune=prune, ai_player=ai_player)

    if algorithm == "minimax":
        best_col, best_val, nodes, root = solver.run_minimax(board)
    elif algorithm == "expectiminimax":
        best_col, best_val, nodes, root = solver.run_expectiminimax(board)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    response_data = {
        "algorithm": algorithm,
        "best_col": best_col,
        "value": best_val,
        "nodes_expanded": nodes,
        "tree": root.to_json()
    }

    # print(json.dumps(response_data, indent=4))
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True, port=5050)