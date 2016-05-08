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
import time
import argparse
import sys

from modules.ChessModel import ChessModel
from modules.ChessTable import ChessTable
from modules.ChessPiece import ChessPiece

def main():
    """
    Main method for calculating unique chess configurations.
    Starts recursive method (find_place) in order to do its work,
    does time tracking and other eye candy things.
    """
    parser = argparse.ArgumentParser(description="""Finds all unique
    configurations of a set of normal chess pieces on a chess board
    """)

    parser.add_argument("x", help="number of columns in chess table", type=int)
    parser.add_argument("y", help="number of rows in chess table", type=int)

    parser.add_argument('--king', type=int,
                   help='Number of kings in configurations')
    parser.add_argument('--queen', type=int,
                   help='Number of queens in configurations')
    parser.add_argument('--rook', type=int,
                   help='Number of rooks in configurations')
    parser.add_argument('--knight', type=int,
                   help='Number of knights in configurations')
    parser.add_argument('--bishop', type=int,
                   help='Number of bishops in configurations')
    parser.add_argument('--render', type=int, default=3,
                   help='Number of tables to render, default = 3')



    args = parser.parse_args()

    time_start = time.time()
    good_config = True
    total_pieces = 0

    X_SIZE = args.x
    Y_SIZE = args.y
    starting_pieces = []


    if(args.king):
        starting_pieces.append([ChessPiece(ChessModel.KING), args.king])
    if(args.queen):
        starting_pieces.append([ChessPiece(ChessModel.QUEEN), args.queen])
    if(args.rook):
        starting_pieces.append([ChessPiece(ChessModel.ROOK), args.rook])
    if(args.knight):
        starting_pieces.append([ChessPiece(ChessModel.KNIGHT), args.knight])
    if(args.bishop):
        starting_pieces.append([ChessPiece(ChessModel.BISHOP), args.bishop])


    table = ChessTable(starting_pieces)
    table.x_size = X_SIZE
    table.y_size = Y_SIZE
    table.prepare()

    if len(starting_pieces) == 0:
        print "You need to add at least one type of chess piece"
        good_config = False

    if table.oneD_table_size < total_pieces:
        print "Not enough tiles for all pieces."
        good_config = False

    if not good_config:
        parser.print_usage()
    else:
        #recursiv
        successful_tables = table.solve()

        if len(successful_tables) > 0:
            print "Latest 3 tables:"
            for i in successful_tables[:args.render]:
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
