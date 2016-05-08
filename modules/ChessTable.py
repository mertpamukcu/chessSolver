import copy

from modules.ChessModel import ChessModel
from modules.list_permutations import perm_unique

class ChessTable(ChessModel):
    """
    Holds and calculates chess table possibilities.

    Attributes:
        starting_pieces: pieces to put on the table
    """

    start_table = []
    successful_tables = []

    starting_pieces = []

    oneD_table_size = 4
    x_size = 2
    y_size = 2

    range_x = []
    range_y = []

    combination_cache = {}
    combination_cache_index = set()

    def __init__(self,starting_pieces):
        self.starting_pieces = starting_pieces

    def prepare(self):
        self.range_x = range(0, self.x_size)
        self.range_y = range(0, self.y_size)
        self.oneD_table_size = self.x_size * self.y_size

        for i in range(0, self.oneD_table_size):
            self.start_table.append(0)

    def solve(self):
        self.find_place(self.start_table, self.starting_pieces, 0)
        return self.successful_tables

    def find_place(self, table, pieces, line):
        """
        A recursive function, takes a single kind of piece,
        finds empty and safe tiles in table, calculates all permutations of that set
        of pieces in empty and safe tiles,iterates over them and if can position all
        pieces in one kind; calls itself for next set of pieces.

        Args:
            table (List): Latest status of table
            pieces: List of pieces waiting to be positioned on table.
            line (int): for determining kind of piece to position in current step.
        """

        temp_table = copy.copy(table)
        piece_count = pieces[line][1]

        #make a smaller table, just empty tiles
        empty_tiles_table = []
        for tile in temp_table:
            if tile == 0:
                empty_tiles_table.append(0)

        good_table = True

        if piece_count <= len(empty_tiles_table):
            for i in range(0, piece_count):
                empty_tiles_table[i] = 9
        else:
            #it means table dont have any more rooms for remaining pieces.
            good_table = False

        table_for_start_of_round = copy.copy(table)
        if str(empty_tiles_table) in self.combination_cache_index:
            combinations_for_piece = self.combination_cache[str(empty_tiles_table)]
        else:
            combinations_for_piece = perm_unique(empty_tiles_table)
            self.combination_cache[str(empty_tiles_table)] = combinations_for_piece
            self.combination_cache_index.add(str(empty_tiles_table))

        if good_table:
            for combination in combinations_for_piece:
                self.calculate_group(table, table_for_start_of_round, combination, line)

    def find_empty_row_in_table(self, table, line):
        """
        Finds Nth (line) empty tile in table.
        Returns -1 if there aren't enough tiles to put.

        Args:
            table (List): Source table to find empty tile
            line (int): Nth tile to find
        """

        i = 0
        column = 0
        while i < len(table):
            if table[i] == self.SAFE_ZONE:
                if column == line:
                    return i
                else:
                    column += 1
            i += 1
        return -1 #because False == 0 is True


    def calculate_group(self, table, table_for_start_of_round, combination, line):
        """
        Tests a combination of all same kind of pieces,
        and looks for if they are threatening others.
        If calculation successful, passes final table and line + 1 to (find_place)
        to position next kind of pieces. If there aren't any other kind of pieces to
        put in table. Puts table in successful_tables List.

        Args:
            table (List): Latest status of table
            table_for_start_of_round (List): Table without any pieces from current kind.
            combination (List): Contains potential position for current kind of pieces in empty tiles.
            line (int): for passing to calculate_for_piece method.
        """
        successful, table_for_this_round = self.calculate_for_piece(
            table,
            table_for_start_of_round,
            combination,
            line
        )

        if successful and len(self.starting_pieces) - 1 == line:
            self.successful_tables.append(table_for_this_round)
            return table_for_this_round

        elif successful:
            self.find_place(table_for_this_round, self.starting_pieces, line + 1)
            return True

        else:
            return False

    def calculate_for_piece(self, table, table_for_start_of_round, combination, line):
        """
        Tests one piece in combination for single kind of pieces,
        and looks for if they are threatening others.
        Returns a List having piece positioned and calculated threats to other pieces,
        and a boolean that returns False, if one of the pieces in final table threatening another.

        Args:
            table (List): Latest status of table
            table_for_start_of_round (List): Table without any pieces from current kind.
            combination (List): Contains potential position for current kind of pieces in empty tiles.
            line (int): for determining current piece in combination.
        """
        table_for_this_round = copy.copy(table)
        successful = True

        for k, value in enumerate(combination):
            empty_row_in_main_table = self.find_empty_row_in_table(table_for_start_of_round, k)

            if (table_for_this_round[empty_row_in_main_table] == 0
                    and value > 0
                    and empty_row_in_main_table > -1):

                table_for_this_round[empty_row_in_main_table] = self.starting_pieces[line][0]

                #calculates threat squares
                danger_zoned_table = self.fill_danger_zones(
                    table_for_this_round,
                    self.starting_pieces[line][0],
                    empty_row_in_main_table
                )
                #and returns False if a piece is already threated by it
                if not danger_zoned_table:
                    successful = False
                else:
                    table_for_this_round = danger_zoned_table

            elif value > 0 or not empty_row_in_main_table > -1:
                successful = False

        return successful, table_for_this_round

    def render_table(self, table1d):
        """
        Converts a list to 2D and returns a string looks a like chessboard.

        Args:
            table1d (List): one dimensional chess table.

        """
        drawline = ""
        table = [[0 for x_pos in range(self.x_size)] for y_pos in range(self.y_size)]
        index1d = 0
        for x_pos in range(0, self.x_size):
            for y_pos in range(0, self.y_size):
                table[x_pos][y_pos] = table1d[index1d]
                index1d += 1

        for x_pos in range(0, self.x_size):
            for y_pos in range(0, self.y_size):
                if table[x_pos][y_pos] == self.SAFE_ZONE:
                    table[x_pos][y_pos] = "."

                if table[x_pos][y_pos] == self.DANGER_ZONE:
                    table[x_pos][y_pos] = "."

                if table[x_pos][y_pos] == self.ROOK:
                    table[x_pos][y_pos] = "R"

                if table[x_pos][y_pos] == self.KING:
                    table[x_pos][y_pos] = "K"

                if table[x_pos][y_pos] == self.KNIGHT:
                    table[x_pos][y_pos] = "N"

                if table[x_pos][y_pos] == self.BISHOP:
                    table[x_pos][y_pos] = "B"

                if table[x_pos][y_pos] == self.QUEEN:
                    table[x_pos][y_pos] = "Q"

                drawline += "|" + str(table[x_pos][y_pos]) + ""
            drawline += "\n"
        return drawline
