import unittest
from modules.ChessPiece import ChessPiece
from modules.ChessTable import ChessTable

class TestChessPieceFunctions(unittest.TestCase):
    X_SIZE = 4
    Y_SIZE = 4

    def test_bishop_danger_zones(self):
        test_table = ChessTable()
        test_table.x_size = self.X_SIZE
        test_table.y_size = self.Y_SIZE
        test_table.prepare()

        piece = ChessPiece(ChessPiece.BISHOP)
        test_table.start_table[10] = piece

        true_result = [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, piece, 0], [0, 1, 0, 1]]

        self.assertEqual(piece.bishop_danger_zones(test_table, 2, 2).get_2d_table(),
                true_result,
                "Bishops threating wrong tiles")

    def test_rook_danger_zones(self):
        test_table = ChessTable()
        test_table.x_size = self.X_SIZE
        test_table.y_size = self.Y_SIZE
        test_table.prepare()

        piece = ChessPiece(ChessPiece.ROOK)
        test_table.start_table[10] = piece

        true_result = [[0, 0, 1, 0], [0, 0, 1, 0], [1, 1, piece, 1], [0, 0, 1, 0]]

        self.assertEqual(piece.rook_danger_zones(test_table, 2, 2).get_2d_table(),
                true_result,
                "Rook threating wrong tiles")

    def test_knight_danger_zones(self):
        test_table = ChessTable()
        test_table.x_size = self.X_SIZE
        test_table.y_size = self.Y_SIZE
        test_table.prepare()

        piece = ChessPiece(ChessPiece.KNIGHT)
        test_table.start_table[10] = piece

        true_result = [[0, 1, 0, 1], [1, 0, 0, 0], [0, 0, piece, 0], [1, 0, 0, 0]]

        self.assertEqual(piece.knight_danger_zones(test_table, 2, 2).get_2d_table(),
                true_result,
                "Knight threating wrong tiles")

    def test_king_danger_zones(self):
        test_table = ChessTable()
        test_table.x_size = self.X_SIZE
        test_table.y_size = self.Y_SIZE
        test_table.prepare()

        piece = ChessPiece(ChessPiece.KING)
        test_table.start_table[10] = piece

        true_result = [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, piece, 1], [0, 1, 1, 1]]

        self.assertEqual(piece.king_danger_zones(test_table, 2, 2).get_2d_table(),
                true_result,
                "King threating wrong tiles")

    def test_fill_danger_zones(self):
        test_table = ChessTable()
        test_table.x_size = self.X_SIZE
        test_table.y_size = self.Y_SIZE
        test_table.prepare()

        queen = ChessPiece(ChessPiece.QUEEN)

        line = 5
        test_table.start_table[line] = queen

        true_result = [1, 1, 1, 0, 1, queen, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1]

        self.assertEqual(queen.fill_danger_zones(test_table, line).start_table,
                true_result,
                "There is a problem in fill_danger_zones")
