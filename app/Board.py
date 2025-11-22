from typing import List

ROWS = 6
COLS = 7

class Board:
    __slots__ = ("__p1", "__p2", "__free")

    def __init__(self,
                 matrix: List[List[int]] | None = None,
                 p1: bytearray | None = None,
                 p2: bytearray | None = None,
                 free_positions: bytearray | None = None):
        """
        Initialize a Connect4 board.

        Parameters:
        - matrix: Optional ROWS x COLS matrix (0=empty, 1=player1, 2=player2)
        - p1, p2, free_positions: Optional internal representation (bitboards)
        """
        if matrix is not None:
            self.load_from_matrix(matrix)
            return

        self.__p1 = p1.copy() if p1 is not None else bytearray(ROWS)
        self.__p2 = p2.copy() if p2 is not None else bytearray(ROWS)
        self.__free = free_positions.copy() if free_positions is not None else bytearray(COLS)

    def load_from_matrix(self, matrix: List[List[int]]):
        """
        Load board state from a ROWS x COLS integer matrix.

        Updates internal bitboards (__p1, __p2) and free positions (__free).

        Raises:
            ValueError: if matrix values are incorrect.
        """
        self.__p1 = bytearray(ROWS)
        self.__p2 = bytearray(ROWS)
        self.__free = bytearray(COLS)

        for r in range(ROWS):
            for c in range(COLS):
                val = matrix[r][c]
                if r < ROWS - 1 and val == 0 and matrix[r + 1][c] != 0:
                    raise ValueError(f"Invalid Board: There is an empty slot between to two tiles at board[{r}][{c}] = {matrix[r][c]}")
                if val == 1:
                    self.play(c, True)
                elif val == 2:
                    self.play(c, False)

    def copy(self) -> "Board":
        return Board(p1=self.__p1, p2=self.__p2, free_positions=self.__free)

    @property
    def p1(self) -> bytearray:
        return self.__p1.copy()

    @property
    def p2(self) -> bytearray:
        return self.__p2.copy()

    @property
    def free_positions(self) -> bytearray:
        return self.__free.copy()

    def free_position(self, i: int) -> int:
        return self.__free[i]

    def legal_moves(self) -> List[int]:
        return [c for c in range(COLS) if self.__free[c] < ROWS]

    def play(self, col: int, player: bool) -> None:
        """
        Make a move for the given player in the specified column.

        Parameters:
        - col: Column to play (0-based)
        - player: True for player1, False for player2

        Raises:
            ValueError: if column is invalid or full.
        """
        if not (0 <= col < COLS):
            raise ValueError(f"Column out of range: {col}")

        row = self.__free[col]
        if row >= ROWS:
            raise ValueError(f"Column {col} is full")

        if player:
            self.__p1[row] |= (1 << col)
        else:
            self.__p2[row] |= (1 << col)

        self.__free[col] = row + 1

    def apply_action(self, col: int, player: bool) -> "Board":
        """
        Return a new Board with the move applied.
        """
        applied_board = self.copy()
        applied_board.play(col, player)
        return applied_board

    def neighbours(self, player: bool) -> List["Board"]:
        """Return all possible next boards for the given player (non-mutating)."""
        return [self.apply_action(c, player) for c in range(COLS) if self.__free[c] < ROWS]

    def is_terminal(self) -> bool:
        """Return True if the board is full (no legal moves left)."""
        return all(f >= ROWS for f in self.__free)

    def utility(self) -> int:
        """
        Compute utility value: number of 4-in-a-rows for player1 minus player2.
        Useful for evaluating immediate wins/losses.
        """
        return self.count_connected(True) - self.count_connected(False)

    def count_connected(self, player: bool) -> int:
        """
        Count all 4-in-a-row occurrences for a given player.

        Includes horizontal, vertical, and diagonal connections.
        Overlapping connections are counted separately.
        """
        bit_rows = self.__p1 if player else self.__p2
        count = 0

        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(((bit_rows[r] >> (c + i)) & 1) for i in range(4)):
                    count += 1

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(((bit_rows[r + i] >> c) & 1) for i in range(4)):
                    count += 1

        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(((bit_rows[r + i] >> (c + i)) & 1) for i in range(4)):
                    count += 1

        # Diagonal down-left
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if all(((bit_rows[r + i] >> (c - i)) & 1) for i in range(4)):
                    count += 1

        return count

    def to_matrix(self) -> List[List[int]]:
        """
        Convert internal bitboards to a ROWS x COLS matrix.

        Returns:
            2D list with values:
                0 = empty
                1 = player1
                2 = player2
        """
        mat = [[0] * COLS for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if (self.__p1[r] >> c) & 1:
                    mat[r][c] = 1
                elif (self.__p2[r] >> c) & 1:
                    mat[r][c] = 2
        return mat

    def __repr__(self) -> str:
        """
        Human-readable string representation.
        Top row first, using:
            X = player1
            O = player2
            . = empty
        """
        rows = []
        for r in reversed(range(ROWS)):
            row_chars = []
            for c in range(COLS):
                if (self.__p1[r] >> c) & 1:
                    row_chars.append("X")
                elif (self.__p2[r] >> c) & 1:
                    row_chars.append("O")
                else:
                    row_chars.append(".")
            rows.append(" ".join(row_chars))
        return "\n".join(rows)
