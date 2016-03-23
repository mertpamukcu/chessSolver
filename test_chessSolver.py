import unittest
import chessSolver

class TestChessSolverFunctions(unittest.TestCase):
    X_SIZE = 4
    Y_SIZE = 4

    chessSolver.X_SIZE = X_SIZE
    chessSolver.Y_SIZE = Y_SIZE
    chessSolver.range_x = range(0, X_SIZE)
    chessSolver.range_y = range(0, Y_SIZE)

    def test_bishop_danger_zones(self):
        table = [[0 for x_pos in range(self.X_SIZE)] for y_pos in range(self.Y_SIZE)]
        table[2][2] = chessSolver.BISHOP

        true_result = [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 6, 0], [0, 1, 0, 1]]

        self.assertEqual(chessSolver.bishop_danger_zones(table, 2, 2),
                true_result,
                "Bishops threating wrong tiles")

    def test_rook_danger_zones(self):
        table = [[0 for x_pos in range(self.X_SIZE)] for y_pos in range(self.Y_SIZE)]
        table[2][2] = chessSolver.ROOK

        true_result = [[0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 2, 1], [0, 0, 1, 0]]

        self.assertEqual(chessSolver.rook_danger_zones(table, 2, 2),
                true_result,
                "Rook threating wrong tiles")

    def test_knight_danger_zones(self):
        table = [[0 for x_pos in range(self.X_SIZE)] for y_pos in range(self.Y_SIZE)]
        table[2][2] = chessSolver.KNIGHT

        true_result = [[0, 1, 0, 1], [1, 0, 0, 0], [0, 0, 3, 0], [1, 0, 0, 0]]

        self.assertEqual(chessSolver.knight_danger_zones(table, 2, 2),
                true_result,
                "Knight threating wrong tiles")

    def test_king_danger_zones(self):
        table = [[0 for x_pos in range(self.X_SIZE)] for y_pos in range(self.Y_SIZE)]
        table[2][2] = chessSolver.KING

        true_result = [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 4, 1], [0, 1, 1, 1]]

        self.assertEqual(chessSolver.king_danger_zones(table, 2, 2),
                true_result,
                "King threating wrong tiles")

    def test_fill_danger_zones(self):
        table = [0 for x_pos in range(self.X_SIZE * self.Y_SIZE)]
        piece = chessSolver.QUEEN
        line = 5
        table[line] = piece
        true_result = [1, 1, 1, 0, 1, 5, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1]

        self.assertEqual(chessSolver.fill_danger_zones(table, piece, line),
                true_result,
                "There is a problem in fill_danger_zones")

    def test_calculate_group(self):
        chessSolver.STARTING_PIECES = [[chessSolver.QUEEN, 2]]
        table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        table_for_start_of_round = [0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0]

        #lets start with queens
        combination = [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1]
        line = 0
        self.assertEqual(
            chessSolver.calculate_group(table, table_for_start_of_round,
                combination, line),
            true_result,
            "Didn't returned correct table")

        #impossible combination should result false
        combination = [0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0]
        true_result = False
        self.assertEqual(
            chessSolver.calculate_group(table, table_for_start_of_round,
                combination, line),
            true_result,
            "Didn't return False for impossible table")

        #is going findout to next piece kind
        chessSolver.STARTING_PIECES = [[chessSolver.QUEEN, 2],
            [chessSolver.ROOK, 1]]
        combination = [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0]
        true_result = True

        self.assertEqual(
            chessSolver.calculate_group(table, table_for_start_of_round,
                combination, line),
            true_result,
            "Didn't start recursive function")

    def test_calculate_for_piece(self):
        chessSolver.STARTING_PIECES = [[chessSolver.QUEEN, 2]]
        table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        table_for_start_of_round = [0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0]

        #trying a possible combination
        combination = [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1]
        line = 0

        successful, table_for_this_round = chessSolver.calculate_for_piece(
            table,
            table_for_start_of_round,
            combination,
            line
        )

        #trying an impossible combination
        true_result = (True, [1, 1, 1, 0, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1])
        self.assertEqual((successful, table_for_this_round),true_result)

        combination = [0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0]
        true_result = [1, 1, 1, 0, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1]
        line = 0

        true_result = (False, [1, 1, 0, 0, 5, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0])

        successful, table_for_this_round = chessSolver.calculate_for_piece(
            table,
            table_for_start_of_round,
            combination,
            line
        )

        self.assertEqual((successful, table_for_this_round),true_result)

    def test_render_table(self):
        """
        just for fun
        """

        table = [1, 1, 2, 3, 4, 5, 6, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        true_render = "|.|.|R|N\n|K|Q|B|.\n|.|.|.|.\n|.|.|.|.\n"

        self.assertEqual(chessSolver.render_table(table),true_render)

if __name__ == '__main__':
    unittest.main(exit=False)
