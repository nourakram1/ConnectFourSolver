import unittest
from app.Board import Board, ROWS, COLS

class BoardTest(unittest.TestCase):

    def test_empty_board(self):
        b = Board()
        for r in range(ROWS):
            for c in range(COLS):
                self.assertEqual((b.p1[r] >> c) & 1, 0)
                self.assertEqual((b.p2[r] >> c) & 1, 0)
        self.assertEqual(b.legal_moves(), list(range(COLS)))
        self.assertFalse(b.is_terminal())
        self.assertEqual(b.utility(), 0)

    def test_play_one_piece(self):
        b = Board()
        b.play(3, True)
        self.assertEqual(b.p1[0] >> 3 & 1, 1)
        self.assertEqual(b.p2[0] >> 3 & 1, 0)
        self.assertEqual(b.free_positions[3], 1)

    def test_play_two_players(self):
        b = Board()
        b.play(3, True)
        b.play(3, False)
        self.assertEqual(b.p1[0] >> 3 & 1, 1)
        self.assertEqual(b.p2[1] >> 3 & 1, 1)
        self.assertEqual(b.free_positions[3], 2)

    def test_apply_action_returns_new_board(self):
        b = Board()
        b2 = b.apply_action(2, True)
        self.assertNotEqual(id(b), id(b2))
        self.assertEqual(b.p1[0] >> 2 & 1, 0)
        self.assertEqual(b2.p1[0] >> 2 & 1, 1)

    def test_neighbours(self):
        b = Board()
        neigh = b.neighbours(True)
        self.assertEqual(len(neigh), COLS)
        for n in neigh:
            self.assertEqual(n.free_positions.count(0), COLS - 1)

    def test_full_column(self):
        b = Board()
        for _ in range(ROWS):
            b.play(0, True)
        self.assertEqual(b.free_positions[0], ROWS)
        self.assertNotIn(0, b.legal_moves())
        with self.assertRaises(ValueError):
            b.play(0, False)

    def test_is_terminal_full_board(self):
        b = Board()
        for c in range(COLS):
            for _ in range(ROWS):
                b.play(c, c % 2 == 0)
        self.assertTrue(b.is_terminal())
        self.assertEqual(b.legal_moves(), [])

    # --------------------------
    # Connected-4 tests
    # --------------------------
    def test_horizontal_four(self):
        b = Board()
        for col in range(4):
            b.play(col, True)
        self.assertEqual(b.count_connected(True), 1)
        self.assertEqual(b.utility(), 1)

    def test_vertical_four(self):
        b = Board()
        for _ in range(4):
            b.play(2, True)
        self.assertEqual(b.count_connected(True), 1)

    def test_diagonal_down_right(self):
        b = Board()
        b.play(0, True)
        b.play(1, False); b.play(1, True)
        b.play(2, False); b.play(2, False); b.play(2, True)
        b.play(3, False); b.play(3, False); b.play(3, False); b.play(3, True)
        self.assertEqual(b.count_connected(True), 1)

    def test_diagonal_down_left(self):
        b = Board()
        b.play(3, True)
        b.play(2, False); b.play(2, True)
        b.play(1, False); b.play(1, False); b.play(1, True)
        b.play(0, False); b.play(0, False); b.play(0, False); b.play(0, True)
        self.assertEqual(b.count_connected(True), 1)

    def test_no_false_four(self):
        b = Board()
        b.play(0, True)
        b.play(1, True)
        b.play(2, True)
        self.assertEqual(b.count_connected(True), 0)

    def test_mixed_players_no_cross_detection(self):
        b = Board()
        b.play(0, True)
        b.play(1, False)
        b.play(2, True)
        b.play(3, False)
        self.assertEqual(b.count_connected(True), 0)
        self.assertEqual(b.count_connected(False), 0)
        self.assertEqual(b.utility(), 0)

    def test_copy_board_independence(self):
        b = Board()
        b.play(3, True)
        c = b.copy()
        c.play(2, False)
        self.assertEqual(b.p1[0] >> 3 & 1, 1)
        self.assertEqual(b.p2[0] >> 2 & 1, 0)
        self.assertEqual(c.p2[0] >> 2 & 1, 1)

    # -----------------------------------------
    #         Utility-specific tests
    # -----------------------------------------

    def test_utility_horizontal_x(self):
        b = Board()
        for c in range(4):
            b.play(c, True)
        self.assertEqual(b.utility(), 1)

    def test_utility_vertical_x(self):
        b = Board()
        for _ in range(4):
            b.play(6, True)
        self.assertEqual(b.utility(), 1)

    def test_utility_diagonal_x(self):
        b = Board()
        b.play(0, True)
        b.play(1, False); b.play(1, True)
        b.play(2, False); b.play(2, False); b.play(2, True)
        b.play(3, False); b.play(3, False); b.play(3, False); b.play(3, True)
        self.assertEqual(b.utility(), 1)

    def test_utility_two_wins_x(self):
        b = Board()
        # Two horizontal wins stacked
        for c in range(4):
            b.play(c, True)
        for c in range(4):
            b.play(c, True)
        self.assertEqual(b.utility(), 2)

    def test_utility_one_x_one_o(self):
        b = Board()
        for c in range(4):
            b.play(c, True)   # X horizontal
        for _ in range(4):
            b.play(6, False)  # O vertical
        self.assertEqual(b.utility(), 0)

    def test_utility_no_wins(self):
        b = Board()
        b.play(0, True)
        b.play(1, False)
        b.play(2, True)
        b.play(3, False)
        self.assertEqual(b.utility(), 0)

    def test_empty_matrix(self):
        """Board initialized with all zeros should be empty."""
        mat = [[0] * COLS for _ in range(ROWS)]
        b = Board(matrix=mat)
        for r in range(ROWS):
            for c in range(COLS):
                self.assertEqual((b.p1[r] >> c) & 1, 0)
                self.assertEqual((b.p2[r] >> c) & 1, 0)
        self.assertEqual(b.legal_moves(), list(range(COLS)))
        self.assertFalse(b.is_terminal())


    def test_full_column_matrix(self):
        """Board initialized with a full column."""
        mat = [[0] * COLS for _ in range(ROWS)]
        for r in range(ROWS):
            mat[r][4] = 1 if r % 2 == 0 else 2
        b = Board(matrix=mat)
        self.assertEqual(b.free_positions[4], ROWS)
        self.assertNotIn(4, b.legal_moves())

if __name__ == "__main__":
    unittest.main()
