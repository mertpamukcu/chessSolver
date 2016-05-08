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

from modules.ChessModel import ChessModel
from modules.ChessTable import ChessTable
from modules.ChessPiece import ChessPiece

def main():
    """
    Main method for calculating unique chess configurations.
    Starts recursive method (find_place) in order to do its work,
    does time tracking and other eye candy things.
    """
    time_start = time.time()
    good_config = True
    total_pieces = 0

    X_SIZE = 4
    Y_SIZE = 4
    STARTING_PIECES = [[ChessPiece(ChessModel.ROOK), 2], [ChessPiece(ChessModel.KNIGHT),4]]

    table = ChessTable(STARTING_PIECES)
    table.x_size = X_SIZE
    table.y_size = Y_SIZE
    table.prepare()

    if table.oneD_table_size < total_pieces:
        print "Not enough tiles for all pieces."
        good_config = False

    if not good_config:
        print "Configuration Error"
    else:
        #recursiv
        successful_tables = table.solve()

        if len(successful_tables) > 0:
            print "Latest 3 tables:"
            for i in successful_tables[:3]:
                print i.render_table()

            print "Total possibilities:"
            print len(successful_tables)

            print "Time in seconds:"
            time_end = time.time()
            print time_end - time_start
        else:
            print "Couldn't Found any combination"


if __name__ == '__main__':
    main()
