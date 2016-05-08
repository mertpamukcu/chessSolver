import unittest
from modules.ChessPiece import ChessPiece
from modules.ChessTable import ChessTable

class TestChessPieceFunctions(unittest.TestCase):
    X_SIZE = 4
    Y_SIZE = 4

    def test_get_2d_table(self):
        table = ChessTable([])
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE
        table.start_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        table.prepare()

        true_result = [[0, 1, 2, 3], [4, 5, 6, 7],
            [8, 9, 10, 11], [12, 13, 14, 15]]

        self.assertEqual(
            table.get_2d_table(),
            true_result,
            "Didn't returned a version of same table")

    def test_convert_2d_to_1d(self):
        table = ChessTable()
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE

        table2d = [[0, 1, 2, 3], [4, 5, 6, 7],
                [8, 9, 10, 11], [12, 13, 14, 15]]
        result = table.convert_2d_to_1d(table2d)
        true_result = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

        self.assertEqual(
            result,
            true_result,
            "Didn't return a version of same table")


    def test_calculate_group(self):
        queen = ChessPiece(ChessPiece.QUEEN)
        rook = ChessPiece(ChessPiece.ROOK)

        starting_pieces = [[queen, 2]]
        table = ChessTable(starting_pieces)
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE
        table.prepare()

        table_for_start_of_round = ChessTable()
        table_for_start_of_round.x_size = self.X_SIZE
        table_for_start_of_round.y_size = self.Y_SIZE
        table_for_start_of_round.prepare()

        #lets start with queens
        combination = [0, 0, 0, 0, queen, 0, 0, 0, 0, 0, queen, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, queen, 1, 1, 1, 1, 1, queen, 1, 1, 1, 1, 1]
        line = 0

        self.assertEqual(
            table.calculate_group(table, table_for_start_of_round,
                combination,
                line).start_table ,
            true_result,
            "Didn't returned correct table")

        #impossible combination should result false
        combination = [0, 0, 0, 0, queen, 0, 0, 0, 0, queen, 0, 0, 0, 0, 0, 0]
        true_result = False
        self.assertEqual(
            table.calculate_group(table, table_for_start_of_round,
                combination, line),
            true_result,
            "Didn't return False for impossible table")

        #is going findout to next piece kind
        starting_pieces = [
            [queen, 2],
            [rook, 1]]

        table = ChessTable(starting_pieces)
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE
        table.prepare()

        combination = [0, 0, 0, 0, queen, 0, 0, 0, 0, 0, queen, 0, 0, 0, 0, 0]
        true_result = True

        self.assertEqual(
            table.calculate_group(table, table_for_start_of_round,
                combination, line),
            true_result,
            "Didn't start recursive function")

    def test_calculate_for_piece(self):
        queen = ChessPiece(ChessPiece.QUEEN)

        starting_pieces = [[queen, 2]]
        table = ChessTable(starting_pieces)
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE
        table.prepare()

        table_for_start_of_round = ChessTable()
        table_for_start_of_round.x_size = self.X_SIZE
        table_for_start_of_round.y_size = self.Y_SIZE
        table_for_start_of_round.prepare()

        #trying a possible combination
        combination = [0, 0, 0, 0, queen, 0, 0, 0, 0, 0, queen, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, queen, 1, 1, 1, 1, 1, queen, 1, 1, 1, 1, 1]
        line = 0

        successful, table_for_this_round = table.calculate_for_piece(
            table,
            table_for_start_of_round,
            combination,
            line
        )

        #trying an impossible combination
        true_result = (True, [1, 1, 1, 0, queen, 1, 1, 1, 1, 1, queen, 1, 1, 1, 1, 1])
        self.assertEqual((successful, table_for_this_round.start_table),true_result)

        combination = [0, 0, 0, 0, queen, 0, 0, 0, 0, queen, 0, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, queen, 1, 1, 1, 1, 1, queen, 1, 1, 1, 1, 1]
        line = 0

        true_result = (False, [1, 1, 0, 0, queen, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0])

        successful, table_for_this_round = table.calculate_for_piece(
            table,
            table_for_start_of_round,
            combination,
            line
        )

        self.assertEqual((successful, table_for_this_round.start_table),true_result)

    def test_render_table(self):
        """
        just for fun
        """
        table = ChessTable([])
        table.x_size = self.X_SIZE
        table.y_size = self.Y_SIZE
        table.prepare()

        queen = ChessPiece(ChessPiece.QUEEN)
        rook = ChessPiece(ChessPiece.ROOK)
        knight = ChessPiece(ChessPiece.KNIGHT)
        king = ChessPiece(ChessPiece.KING)
        bishop = ChessPiece(ChessPiece.BISHOP)

        table.start_table = [1, 1, rook, knight, king, queen, bishop, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        true_render = "|.|.|R|N\n|K|Q|B|.\n|.|.|.|.\n|.|.|.|.\n"

        self.assertEqual(table.render_table(),true_render)
