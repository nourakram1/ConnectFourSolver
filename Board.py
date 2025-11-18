ROWS = 6
COLS = 7

class Board:
    __slots__ = ['__player', '__free_positions']

    def __init__(self, player: bytearray = None, free_positions: bytearray = None):
        self.__player = player.copy() if player is not None else bytearray(ROWS)
        self.__free_positions = free_positions.copy() if free_positions is not None else bytearray(COLS)
        # Getter for player

    @property
    def player(self) -> bytearray:
        return self.__player.copy()

    @property
    def free_positions(self) -> bytearray:
        return self.__free_positions.copy()

    def play(self, col: int, player: bool) -> None:
        row = self.__free_positions[col]
        self.__player[row] |= (int(player) << col)
        self.__free_positions[col] += 1

    def neighbours(self, player) -> list['Board']:
        return [self.apply_action(action, player) for action in self.__free_positions if action < ROWS]

    def apply_action(self, action: int, player: bool) -> 'Board':
        neighbour = Board(self.__player, self.__free_positions)
        neighbour.play(action, player)
        return neighbour

    def is_terminal(self) -> bool:
        return all(free >= ROWS for free in self.__free_positions)

    def utility(self) -> int:
        connected_1s = self.count_connected(True)   # player = True → 1
        connected_0s = self.count_connected(False)  # player = False → 0
        return connected_1s - connected_0s

    def count_connected(self, player: bool) -> int:
        target_bit = int(player)
        count = 0

        # Horizontal check
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(((self.__player[row] >> (col+i)) & 1) == target_bit for i in range(4)):
                    count += 1

        # Vertical check
        for row in range(ROWS - 3):
            for col in range(COLS):
                if all(((self.__player[row+i] >> col) & 1) == target_bit for i in range(4)):
                    count += 1

        # Diagonal ↘
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(((self.__player[row+i] >> (col+i)) & 1) == target_bit for i in range(4)):
                    count += 1

        # Diagonal ↙
        for row in range(ROWS - 3):
            for col in range(3, COLS):
                if all(((self.__player[row+i] >> (col-i)) & 1) == target_bit for i in range(4)):
                    count += 1

        return count