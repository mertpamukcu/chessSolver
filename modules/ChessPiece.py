"""
ChessPiece.py

Created to hold ChessPiece object.

Developed for try-catch challenge
Mert Pamukcu, 2016
"""

from modules.ChessModel import ChessModel

class ChessPiece(ChessModel):
    """
    Used for every chess piece in tables.
    Has functions for calculating potential moves an threats,
    and rendering of itself.
    """
    type = ChessModel.ROOK

    def __init__(self, type):
        self.type = type

    def render_piece(self):
        """
        Returns character representation of pieces.
        For visual needs.
        """
        if self.type == self.ROOK:
            return "R"

        elif self.type == self.KING:
            return "K"

        elif self.type == self.KNIGHT:
            return "N"

        elif self.type == self.BISHOP:
            return "B"

        elif self.type == self.QUEEN:
            return "Q"


    def fill_danger_zones(self, table, line):
        """
        Marks tiles that threatening by current piece as DANGER_ZONE.
        Returns False if position threating an already positioned piece.
        Converts table to 2D List and after calculations converts it again to 1D for
        ease of code.

        Args:
            table (List): Source table to find place
            piece (int): Kind of piece (ROOK,QUEEN etc.)
            line (int): Where to put current piece
        """
        piece = self.type
        origin_x, origin_y = table.get_2d_index(line)

        if piece == self.ROOK:
            table2d = self.rook_danger_zones(table, origin_x, origin_y)

        elif piece == self.BISHOP:
            table2d = self.bishop_danger_zones(table, origin_x, origin_y)

        elif piece == self.QUEEN:
            temp_table = self.bishop_danger_zones(table, origin_x, origin_y)
            if temp_table:
                table2d = self.rook_danger_zones(temp_table, origin_x, origin_y)
            else:
                table2d = False

        elif piece == self.KING:
            table2d = self.king_danger_zones(table, origin_x, origin_y)

        elif piece == self.KNIGHT:
            table2d = self.knight_danger_zones(table, origin_x, origin_y)

        if not table2d:
            return False
        else:
            return table


    def bishop_danger_zones(self, table, origin_x, origin_y):
        """
        Finds bishop's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """
        table2d = table.get_2d_table()

        possible_x = range(-table.x_size, table.x_size)
        possible_y = range(-table.y_size, table.y_size)

        for x_pos in possible_x:
            for y_pos in possible_y:
                if abs(x_pos) == abs(y_pos):
                    target_x = origin_x + x_pos
                    target_y = origin_y + y_pos

                    if not (origin_x == target_x and origin_y == target_y):
                        if target_y in table.range_y and target_x in table.range_x:
                            if table2d[target_x][target_y] in (self.SAFE_ZONE, self.DANGER_ZONE):
                                table2d[target_x][target_y] = self.DANGER_ZONE
                            else:
                                return False

        table.start_table = table.convert_2d_to_1d(table2d)
        return table

    def rook_danger_zones(self, table, origin_x, origin_y):
        """
        Finds Rook's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """
        table2d = table.get_2d_table()

        for target_x in range(0, table.x_size):
            if target_x != origin_x:
                if table2d[target_x][origin_y] == self.SAFE_ZONE or \
                    table2d[target_x][origin_y] == self.DANGER_ZONE:

                    table2d[target_x][origin_y] = self.DANGER_ZONE
                else:
                    return False

        for target_y in range(0, table.y_size):
            if target_y != origin_y:
                if table2d[origin_x][target_y] == self.SAFE_ZONE or \
                    table2d[origin_x][target_y] == self.DANGER_ZONE:

                    table2d[origin_x][target_y] = self.DANGER_ZONE
                else:
                    return False

        table.start_table = table.convert_2d_to_1d(table2d)
        return table

    def king_danger_zones(self, table, origin_x, origin_y):
        """
        Finds King's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """
        table2d = table.get_2d_table()

        older_thread = False
        for x_pos in [-1, 0, 1]:
            for y_pos in [-1, 0, 1]:
                target_y = origin_y + y_pos
                target_x = origin_x + x_pos

                if not (origin_x == target_x and origin_y == target_y): #because its like suicide
                    if target_y in table.range_y and target_x in table.range_x:
                        if table2d[target_x][target_y] in (self.SAFE_ZONE, self.DANGER_ZONE):
                            table2d[target_x][target_y] = self.DANGER_ZONE
                        else:
                            older_thread = True

        if older_thread:
            return False
        else:
            table.start_table = table.convert_2d_to_1d(table2d)
            return table

    def knight_danger_zones(self, table, origin_x, origin_y):
        """
        Finds Knight's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """
        table2d = table.get_2d_table()

        older_thread = False
        all_possible_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                              [1, 2], [1, -2], [-1, 2], [-1, -2]]

        for move in all_possible_moves:
            target_x = origin_x + move[0]
            target_y = origin_y + move[1]

            if not (origin_x == target_x and origin_y == target_y): #suicide again
                if target_y in table.range_y and target_x in table.range_x:
                    if (table2d[target_x][target_y] == self.SAFE_ZONE
                            or table2d[target_x][target_y] == self.DANGER_ZONE):
                        table2d[target_x][target_y] = self.DANGER_ZONE
                    else:
                        older_thread = True

        if older_thread:
            return False
        else:
            table.start_table = table.convert_2d_to_1d(table2d)
            return table
