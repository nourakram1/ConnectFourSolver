from typing import Tuple, Optional
from Board import Board

class Solver:
    @staticmethod
    def solve(board: Board, prune: bool = True):
        return Solver.maximize(board, float('-inf'), float('inf'), prune)[0]

    @staticmethod
    def maximize(board: Board, alpha: float, beta: float, prune: bool) -> Tuple[Optional[Board], int]:
        if board.is_terminal():
            return None, board.utility()

        max_neighbour, max_value = None, float('-inf')

        for neighbour in board.neighbours(True):
            _, value = Solver.minimize(neighbour, alpha, beta, prune)

            if value > max_value:
                max_neighbour, max_value = neighbour, value
            if prune and max_value >= beta :
                break
            if max_value > alpha:
                alpha = max_value

        return max_neighbour, max_value

    @staticmethod
    def minimize(board: Board, alpha: float, beta: float, prune: bool) -> Tuple[Optional[Board], int]:
        if board.is_terminal():
            return None, board.utility()

        min_neighbour, min_value = None, float('inf')

        for neighbour in board.neighbours(False):
            _, value = Solver.maximize(neighbour, alpha, beta)

            if value < min_value:
                min_neighbour, min_value = neighbour, value
            if prune and min_value <= alpha:
                break
            if min_value < beta:
                beta = min_value

        return min_neighbour, min_value