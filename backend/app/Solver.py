from __future__ import annotations  # MUST be first line

from typing import List, Optional, Tuple
import math
from backend.app.Board import Board, ROWS, COLS
from backend.app.BoardEvaluator import BoardEvaluator
from backend.app.MiniMaxTree import MiniMaxTree

class Solver:
    """
    Solver for Connect Four using Minimax or Expectiminimax.

    Attributes:
        depth (int): Max search depth.
        prune (bool): Whether to use alpha-beta pruning.
        ai_player (bool): True if AI is maximizing player.
    """

    def __init__(self, depth: int = 4, prune: bool = True, ai_player: bool = True):
        self.depth = int(depth)
        self.prune = bool(prune)
        self.ai_player = bool(ai_player)

    # -----------------------
    # Public Methods
    # -----------------------
    def run_minimax(self, board: Board, use_prune: Optional[bool] = None) -> Tuple[Optional[int], float, int, MiniMaxTree]:
        """
        Run Minimax search with optional alpha-beta pruning.

        Args:
            board (Board): Current game board.
            use_prune (Optional[bool]): If specified, overrides self.prune.

        Returns:
            Tuple containing:
            - best_col: Best column to play
            - best_val: Heuristic value of that move
            - nodes_expanded: Number of nodes expanded
            - root: Root MiniMaxTree of the search tree
        """
        prune = self.prune if use_prune is None else bool(use_prune)
        return self._choose_minimax(board, self.depth, prune, self.ai_player)

    def run_expectiminimax(self, board: Board, use_prune: Optional[bool] = None) -> Tuple[Optional[int], float, int, MiniMaxTree]:
        """
        Run Expectiminimax search to handle stochastic moves (chance nodes).

        Args:
            board (Board): Current game board.
            use_prune (Optional[bool]): If specified, overrides self.prune.

        Returns:
            Same tuple as run_minimax.
        """
        prune = self.prune if use_prune is None else bool(use_prune)
        return self._choose_expectiminimax(board, self.depth, prune, self.ai_player)

    # -----------------------
    # Internal Minimax Methods
    # -----------------------
    def _choose_minimax(self, board: Board, depth: int, prune: bool, ai_player: bool) -> Tuple[Optional[int], float, int, MiniMaxTree]:
        """Evaluate all moves at root and pick the best one for Minimax."""
        root = MiniMaxTree(move=None, player=None, depth=0)
        nodes = [0]  # Count of nodes expanded
        best_val = -math.inf
        best_col = None
        alpha, beta = -math.inf, math.inf

        for col in board.legal_moves():
            nodes[0] += 1
            child_board = board.apply_action(col, ai_player)
            child_node = MiniMaxTree(move=col, player=ai_player, depth=1)
            root.add_child(child_node)

            val = self._minimax_ab(child_board, depth - 1, alpha, beta, False, prune, ai_player, nodes, child_node)

            if val > best_val:
                best_val = val
                best_col = col

            if prune and best_val >= beta:
                break  # Alpha-beta cutoff

            alpha = max(alpha, best_val)
            root.value = best_val

        return best_col, best_val, nodes[0], root

    def _minimax_ab(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        prune: bool,
        ai_player: bool,
        nodes: List[int],
        node: MiniMaxTree
    ) -> float:
        """Recursive Minimax with alpha-beta pruning and tree building."""
        # Terminal node or depth limit
        if depth == 0 or board.is_terminal():
            val = BoardEvaluator.evaluate(board, ai_player)
            node.value = val
            return val

        if maximizing:
            best = -math.inf
            node.player = ai_player
            for col in board.legal_moves():
                nodes[0] += 1
                child_board = board.apply_action(col, ai_player)
                child_node = MiniMaxTree(move=col, player=ai_player, depth=node.depth + 1)
                node.add_child(child_node)

                val = self._minimax_ab(child_board, depth - 1, alpha, beta, False, prune, ai_player, nodes, child_node)
                best = max(best, val)
                node.value = best

                if prune and best >= beta:
                    return best
                alpha = max(alpha, best)
            return best

        else:  # Minimizing player
            best = math.inf
            node.player = not ai_player
            for col in board.legal_moves():
                nodes[0] += 1
                child_board = board.apply_action(col, not ai_player)
                child_node = MiniMaxTree(move=col, player=not ai_player, depth=node.depth + 1)
                node.add_child(child_node)

                val = self._minimax_ab(child_board, depth - 1, alpha, beta, True, prune, ai_player, nodes, child_node)
                best = min(best, val)
                node.value = best

                if prune and best <= alpha:
                    return best
                beta = min(beta, best)
            return best

    # -----------------------
    # Internal Expectiminimax Methods
    # -----------------------
    def _choose_expectiminimax(self, board: Board, depth: int, prune: bool, ai_player: bool) -> Tuple[
        Optional[int], float, int, MiniMaxTree]:
        """Evaluate all moves at root and pick the best one for Expectiminimax (chance nodes)."""
        nodes = [0]
        root = MiniMaxTree(move=None, player=None, depth=0)
        best_val = -math.inf
        best_col = None
        alpha, beta = -math.inf, math.inf

        def chance_outcomes_for(column: int):
            """Return [(column, probability)] for possible physics outcomes."""
            outcomes = []

            # Chosen column
            chosen_valid = 0 <= column < COLS and board.free_positions[column] < ROWS
            if chosen_valid:
                outcomes.append((column, 0.6))

            # Neighbors
            left_valid = 0 <= column - 1 < COLS and board.free_positions[column - 1] < ROWS
            right_valid = 0 <= column + 1 < COLS and board.free_positions[column + 1] < ROWS

            if left_valid and right_valid:
                outcomes.append((column - 1, 0.2))
                outcomes.append((column + 1, 0.2))
            elif left_valid:
                outcomes.append((column - 1, 0.4))
            elif right_valid:
                outcomes.append((column + 1, 0.4))
            elif chosen_valid:
                outcomes = [(column, 1.0)]

            return outcomes

        for col in board.legal_moves():
            nodes[0] += 1
            chance_node = MiniMaxTree(move=col, player=None, depth=1)
            root.add_child(chance_node)

            outcomes = chance_outcomes_for(col)
            if not outcomes:
                continue

            exp_value = 0.0
            for actual_col, prob in outcomes:
                nodes[0] += 1
                child_board = board.apply_action(actual_col, ai_player)
                child_node = MiniMaxTree(move=actual_col, player=ai_player, prob=prob, depth=2)
                chance_node.add_child(child_node)

                val = self._expectiminimax_min(child_board, depth - 1, alpha, beta, prune, ai_player, nodes, child_node)
                exp_value += prob * val

            chance_node.value = exp_value

            if exp_value > best_val:
                best_val = exp_value
                best_col = col

            if prune and best_val >= beta:
                break  # cutoff at root

            alpha = max(alpha, best_val)
            root.value = best_val

        return best_col, best_val, nodes[0], root

    def _expectiminimax_min(self, board: Board, depth: int, alpha: float, beta: float,
                            prune: bool, ai_player: bool, nodes: List[int], node: MiniMaxTree) -> float:
        """Opponent (min) layer for expectiminimax with pruning."""
        if depth == 0 or board.is_terminal():
            val = BoardEvaluator.evaluate(board, ai_player)
            node.value = val
            return val

        best = math.inf
        node.player = not ai_player
        for col in board.legal_moves():
            nodes[0] += 1
            child_board = board.apply_action(col, not ai_player)
            child_node = MiniMaxTree(move=col, player=not ai_player, depth=node.depth + 1)
            node.add_child(child_node)

            val = self._expectiminimax_max(child_board, depth - 1, alpha, beta, prune, ai_player, nodes, child_node)
            best = min(best, val)
            node.value = best

            if prune and best <= alpha:
                return best
            beta = min(beta, best)

        return best

    def _expectiminimax_max(self, board: Board, depth: int, alpha: float, beta: float,
                            prune: bool, ai_player: bool, nodes: List[int], node: MiniMaxTree) -> float:
        """AI (max) layer for expectiminimax with pruning; contains chance nodes."""
        if depth == 0 or board.is_terminal():
            val = BoardEvaluator.evaluate(board, ai_player)
            node.value = val
            return val

        best = -math.inf
        node.player = ai_player

        for col in board.legal_moves():
            nodes[0] += 1
            chance_node = MiniMaxTree(move=col, player=None, depth=node.depth + 1)
            node.add_child(chance_node)

            outcomes = []
            if 0 <= col < COLS and board.free_positions[col] < ROWS:
                outcomes.append((col, 0.6))
            if 0 <= col - 1 < COLS and board.free_positions[col - 1] < ROWS:
                outcomes.append((col - 1, 0.2))
            if 0 <= col + 1 < COLS and board.free_positions[col + 1] < ROWS:
                outcomes.append((col + 1, 0.2))

            total = sum(p for _, p in outcomes)
            exp_val = 0.0
            for actual_col, p in outcomes:
                pnorm = p / total
                nodes[0] += 1
                child_board = board.apply_action(actual_col, ai_player)
                child_node = MiniMaxTree(move=actual_col, player=ai_player, prob=pnorm, depth=node.depth + 2)
                chance_node.add_child(child_node)

                val = self._expectiminimax_min(child_board, depth - 1, alpha, beta, prune, ai_player, nodes, child_node)
                exp_val += pnorm * val

            chance_node.value = exp_val

            best = max(best, exp_val)
            node.value = best

            if prune and best >= beta:
                return best
            alpha = max(alpha, best)

        return best
