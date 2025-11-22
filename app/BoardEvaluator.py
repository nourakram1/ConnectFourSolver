from typing import List
from Board import Board, ROWS, COLS

class BoardEvaluator:
    """
    Static heuristic evaluator for Connect Four boards.

    Evaluates how favorable a board is for a given player (AI or Human).
    Returns a score: higher score means better for the AI player.

    Heuristic combines:
      - 4-in-a-row completions (winning states)
      - Open 3-in-a-row opportunities
      - Open 2-in-a-row opportunities
      - Mobility (number of legal moves)
      - Center column control (strategic advantage)
    """

    WIN_4_WEIGHT = 10_000.0      # Winning 4-in-a-row is critical
    OPEN_3_WEIGHT = 60.0         # Open 3-in-a-row: potential to win
    OPEN_2_WEIGHT = 8.0          # Open 2-in-a-row: small advantage
    MOBILITY_WEIGHT = 1.0        # Extra score for having more moves
    CENTER_WEIGHT = 3.0          # Control of the center column is advantageous

    # -----------------------
    # Public evaluation method
    # -----------------------
    @staticmethod
    def evaluate(board: Board, ai_player: bool) -> float:
        """
        Evaluate the board for the specified player.

        Args:
            board (Board): Current game board.
            ai_player (bool): True if evaluating for AI, False for opponent.

        Returns:
            float: Heuristic score (higher = better for AI).
        """

        # Count 4-in-a-row completions for AI and opponent
        ai4 = board.count_connected(ai_player)
        hum4 = board.count_connected(not ai_player)

        # Count open 3-in-a-row opportunities
        ai3 = BoardEvaluator._count_k_windows(board, 3, ai_player)
        hum3 = BoardEvaluator._count_k_windows(board, 3, not ai_player)

        # Count open 2-in-a-row opportunities
        ai2 = BoardEvaluator._count_k_windows(board, 2, ai_player)
        hum2 = BoardEvaluator._count_k_windows(board, 2, not ai_player)

        # Number of legal moves (mobility)
        mobility = len(board.legal_moves())

        # Center column control: strategic advantage
        center_control = BoardEvaluator._center_control(board, ai_player) - BoardEvaluator._center_control(board, not ai_player)

        # Final heuristic score (weighted sum)
        score = (
            BoardEvaluator.WIN_4_WEIGHT * (ai4 - hum4) +
            BoardEvaluator.OPEN_3_WEIGHT * (ai3 - hum3) +
            BoardEvaluator.OPEN_2_WEIGHT * (ai2 - hum2) +
            BoardEvaluator.MOBILITY_WEIGHT * mobility +
            BoardEvaluator.CENTER_WEIGHT * center_control
        )

        return float(score)

    # -----------------------
    # Internal helper methods
    # -----------------------
    @staticmethod
    def _count_k_windows(board: Board, k: int, player: bool) -> int:
        """
        Count all windows of length 4 with exactly `k` player pieces and no opponent pieces.

        Args:
            board (Board): Current game board.
            k (int): Number of player pieces in the window.
            player (bool): Player to evaluate (AI or opponent).

        Returns:
            int: Number of matching windows.
        """

        # Bitboards for fast computation
        bit_player = board.p1 if player else board.p2
        bit_oppo = board.p2 if player else board.p1

        # Matrix representation of the board for player and opponent
        pmat = [[(bit_player[r] >> c) & 1 for c in range(COLS)] for r in range(ROWS)]
        omat = [[(bit_oppo[r] >> c) & 1 for c in range(COLS)] for r in range(ROWS)]

        count = 0

        # Check all possible 4-cell windows horizontally
        for r in range(ROWS):
            for c in range(COLS - 3):
                if BoardEvaluator._window_matches(pmat, omat, [(r, c + i) for i in range(4)], k):
                    count += 1

        # Check vertically
        for r in range(ROWS - 3):
            for c in range(COLS):
                if BoardEvaluator._window_matches(pmat, omat, [(r + i, c) for i in range(4)], k):
                    count += 1

        # Check diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if BoardEvaluator._window_matches(pmat, omat, [(r + i, c + i) for i in range(4)], k):
                    count += 1

        # Check diagonal down-left
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if BoardEvaluator._window_matches(pmat, omat, [(r + i, c - i) for i in range(4)], k):
                    count += 1

        return count

    @staticmethod
    def _window_matches(pmat: List[List[int]], omat: List[List[int]], positions: List[tuple], k: int) -> bool:
        """
        Check if a window has exactly `k` player pieces and zero opponent pieces.

        Args:
            pmat (List[List[int]]): Player board matrix.
            omat (List[List[int]]): Opponent board matrix.
            positions (List[tuple]): List of cell positions [(r, c), ...].
            k (int): Exact number of player pieces required.

        Returns:
            bool: True if window matches, False otherwise.
        """
        pc = sum(pmat[r][c] for r, c in positions)
        oc = sum(omat[r][c] for r, c in positions)
        return pc == k and oc == 0

    @staticmethod
    def _center_control(board: Board, player: bool) -> int:
        """
        Count number of player pieces in the center column.

        Args:
            board (Board): Current game board.
            player (bool): Player to count pieces for.

        Returns:
            int: Number of pieces in center column.
        """
        center_col = COLS // 2
        bit_player = board.p1 if player else board.p2
        return sum((bit_player[r] >> center_col) & 1 for r in range(ROWS))
