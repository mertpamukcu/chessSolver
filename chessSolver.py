#!/usr/bin/python
"""
chessSolver.py

Finds all unique configurations of a set of normal chess pieces
on a chess board with dimensions MxN where none of the pieces is
in a position to take any of the others.
Assume the colour of the piece does not matter,
and that there are no pawns among the pieces

Please set these values for configuration;
    STARTING_PIECES = [[ROOK, 2],[KNIGHT, 4]] (list)
    X_SIZE = 4 #set for table x size (int)
    Y_SIZE = 4 #set for table y size (int)

Developed for try-catch challenge
Mert Pamukcu, 2016
"""

import copy
import time
from list_permutations import perm_unique

SAFE_ZONE = 0
DANGER_ZONE = 1

ROOK = 2
KNIGHT = 3
KING = 4
QUEEN = 5
BISHOP = 6

#configuration
#example for real question;
#STARTING_PIECES = [[KING, 2], [QUEEN, 2], [BISHOP, 2], [KNIGHT, 1]]
#X_SIZE = 7
#Y_SIZE = 7

STARTING_PIECES = [[ROOK, 2], [KNIGHT, 4]]
X_SIZE = 4 #set for table x size
Y_SIZE = 4 #set for table y size
#end of configuration

start_table = []

range_x = range(0, X_SIZE)
range_y = range(0, Y_SIZE)

combination_cache = {}
combination_cache_index = set()

successful_tables = []

def bishop_danger_zones(table, origin_x, origin_y):
    """
    Finds bishop's threating tiles

    Args:
        table (List): Source table to find threats
        origin_x (int): x position of piece
        origin_y (int): x position of piece
    """

    possible_x = range(-X_SIZE, X_SIZE)
    possible_y = range(-Y_SIZE, Y_SIZE)

    for x_pos in possible_x:
        for y_pos in possible_y:
            if abs(x_pos) == abs(y_pos):
                target_x = origin_x + x_pos
                target_y = origin_y + y_pos

                if not (origin_x == target_x and origin_y == target_y): #dont try to eat yourself
                    if target_y in range_y and target_x in range_x:
                        if table[target_x][target_y] in (SAFE_ZONE, DANGER_ZONE):
                            table[target_x][target_y] = DANGER_ZONE
                        else:
                            return False
    return table

def rook_danger_zones(table, origin_x, origin_y):
    """
    Finds Rook's threating tiles

    Args:
        table (List): Source table to find threats
        origin_x (int): x position of piece
        origin_y (int): x position of piece
    """

    for target_x in range(0, X_SIZE):
        if target_x != origin_x:
            if table[target_x][origin_y] == SAFE_ZONE or table[target_x][origin_y] == DANGER_ZONE:
                table[target_x][origin_y] = DANGER_ZONE
            else:
                return False

    for target_y in range(0, Y_SIZE):
        if target_y != origin_y:
            if table[origin_x][target_y] == SAFE_ZONE or table[origin_x][target_y] == DANGER_ZONE:
                table[origin_x][target_y] = DANGER_ZONE
            else:
                return False

    return table

def king_danger_zones(table, origin_x, origin_y):
    """
    Finds King's threating tiles

    Args:
        table (List): Source table to find threats
        origin_x (int): x position of piece
        origin_y (int): x position of piece
    """

    older_thread = False
    for x_pos in [-1, 0, 1]:
        for y_pos in [-1, 0, 1]:
            target_y = origin_y + y_pos
            target_x = origin_x + x_pos

            if not (origin_x == target_x and origin_y == target_y): #because its like suicide
                if target_y in range_y and target_x in range_x:
                    if table[target_x][target_y] in (SAFE_ZONE, DANGER_ZONE):
                        table[target_x][target_y] = DANGER_ZONE
                    else:
                        older_thread = True

    if older_thread:
        return False
    else:
        return table

def knight_danger_zones(table, origin_x, origin_y):
    """
    Finds Knight's threating tiles

    Args:
        table (List): Source table to find threats
        origin_x (int): x position of piece
        origin_y (int): x position of piece
    """

    older_thread = False
    all_possible_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                          [1, 2], [1, -2], [-1, 2], [-1, -2]]

    for move in all_possible_moves:
        target_x = origin_x + move[0]
        target_y = origin_y + move[1]

        if not (origin_x == target_x and origin_y == target_y): #suicide again
            if target_y in range_y and target_x in range_x:
                if (table[target_x][target_y] == SAFE_ZONE
                        or table[target_x][target_y] == DANGER_ZONE):
                    table[target_x][target_y] = DANGER_ZONE
                else:
                    older_thread = True

    if older_thread:
        return False
    else:
        return table

def fill_danger_zones(table, piece, line):
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

    table2d = [[0 for x_pos in range(X_SIZE)] for y_pos in range(Y_SIZE)]
    index1d = 0
    for x_pos in range(0, X_SIZE):
        for y_pos in range(0, Y_SIZE):
            if table[index1d] != 0:
                table2d[x_pos][y_pos] = table[index1d]

            if index1d == line:
                origin_x = x_pos
                origin_y = y_pos
            index1d += 1

    if piece == ROOK:
        table2d = rook_danger_zones(table2d, origin_x, origin_y)

    elif piece == BISHOP:
        table2d = bishop_danger_zones(table2d, origin_x, origin_y)

    elif piece == QUEEN:
        table2d = bishop_danger_zones(table2d, origin_x, origin_y)
        if table2d:
            table2d = rook_danger_zones(table2d, origin_x, origin_y)

    elif piece == KING:
        table2d = king_danger_zones(table2d, origin_x, origin_y)

    elif piece == KNIGHT:
        table2d = knight_danger_zones(table2d, origin_x, origin_y)

    if not table2d:
        return False
    else:
        #take table back to 1Dimensional space
        index1d = 0
        for x_pos in range(0, X_SIZE):
            for y_pos in range(0, Y_SIZE):
                table[index1d] = table2d[x_pos][y_pos]
                index1d += 1

        return table

def find_empty_row_in_table(table, line):
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
        if table[i] == SAFE_ZONE:
            if column == line:
                return i
            else:
                column += 1
        i += 1
    return -1 #because False == 0 is True

def find_place(table, pieces, line):
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
    if str(empty_tiles_table) in combination_cache_index:
        combinations_for_piece = combination_cache[str(empty_tiles_table)]
    else:
        combinations_for_piece = perm_unique(empty_tiles_table)
        combination_cache[str(empty_tiles_table)] = combinations_for_piece
        combination_cache_index.add(str(empty_tiles_table))

    if good_table:
        for combination in combinations_for_piece:
            calculate_group(table, table_for_start_of_round, combination, line)

def calculate_group(table, table_for_start_of_round, combination, line):
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
    successful, table_for_this_round = calculate_for_piece(
        table,
        table_for_start_of_round,
        combination,
        line
    )

    if successful and len(STARTING_PIECES) - 1 == line:
        successful_tables.append(table_for_this_round)
        return table_for_this_round

    elif successful:
        find_place(table_for_this_round, STARTING_PIECES, line + 1)
        return True

    else:
        return False

def calculate_for_piece(table, table_for_start_of_round, combination, line):
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
        empty_row_in_main_table = find_empty_row_in_table(table_for_start_of_round, k)

        if (table_for_this_round[empty_row_in_main_table] == 0
                and value > 0
                and empty_row_in_main_table > -1):

            table_for_this_round[empty_row_in_main_table] = STARTING_PIECES[line][0]

            #calculates threat squares
            danger_zoned_table = fill_danger_zones(
                table_for_this_round,
                STARTING_PIECES[line][0],
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

def render_table(table1d):
    """
    Converts a list to 2D and returns a string looks a like chessboard.

    Args:
        table1d (List): one dimensional chess table.

    """
    drawline = ""
    table = [[0 for x_pos in range(X_SIZE)] for y_pos in range(Y_SIZE)]
    index1d = 0
    for x_pos in range(0, X_SIZE):
        for y_pos in range(0, Y_SIZE):
            table[x_pos][y_pos] = table1d[index1d]
            index1d += 1

    for x_pos in range(0, X_SIZE):
        for y_pos in range(0, Y_SIZE):
            if table[x_pos][y_pos] == SAFE_ZONE:
                table[x_pos][y_pos] = "."

            if table[x_pos][y_pos] == DANGER_ZONE:
                table[x_pos][y_pos] = "."

            if table[x_pos][y_pos] == ROOK:
                table[x_pos][y_pos] = "R"

            if table[x_pos][y_pos] == KING:
                table[x_pos][y_pos] = "K"

            if table[x_pos][y_pos] == KNIGHT:
                table[x_pos][y_pos] = "N"

            if table[x_pos][y_pos] == BISHOP:
                table[x_pos][y_pos] = "B"

            if table[x_pos][y_pos] == QUEEN:
                table[x_pos][y_pos] = "Q"

            drawline += "|" + str(table[x_pos][y_pos]) + ""
        drawline += "\n"
    return drawline

def main():
    """
    Main method for calculating unique chess configurations.
    Starts recursive method (find_place) in order to do its work,
    does time tracking and other eye candy things.
    """
    time_start = time.time()
    good_config = True

    total_pieces = 0
    oneD_table_size = X_SIZE * Y_SIZE

    for i in STARTING_PIECES:
        total_pieces += i[1]
        if not i[0] in (ROOK,KNIGHT,BISHOP,KING,QUEEN):
            print "Wrong piece type: " + str(i[0])
            good_config = False

    if oneD_table_size < total_pieces:
        print "Not enough tiles for all pieces."
        good_config = False

    if not good_config:
        print "Configuration Error"
    else:
        for i in range(0, oneD_table_size):
            start_table.append(0)

        #recursiv
        find_place(start_table, STARTING_PIECES, 0)

        if len(successful_tables) > 0:
            print "Latest 3 tables:"
            for i in successful_tables[:3]:
                print render_table(i)

            print "Total possibilities:"
            print len(successful_tables)

            print "Time in seconds:"
            time_end = time.time()
            print time_end - time_start
        else:
            print "Couldn't Found any combination"


if __name__ == '__main__':
    main()
