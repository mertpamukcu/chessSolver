#!/usr/bin/python
"""
chesssolver.py - changed something

Finds all unique configurations of a set of normal chess pieces
on a chess board with dimensions MxN where none of the pieces is
in a position to take any of the others.
Assume the colour of the piece does not matter,
and that there are no pawns among the pieces

For usage details;
chesssolver.py --help

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
    time_start = time.time()

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

    #pieces configuration
    total_pieces = 0
    starting_pieces = []
    if args.king:
        starting_pieces.append([ChessPiece(ChessModel.KING), args.king])
        total_pieces += args.king
    if args.queen:
        starting_pieces.append([ChessPiece(ChessModel.QUEEN), args.queen])
        total_pieces += args.queen
    if args.rook:
        starting_pieces.append([ChessPiece(ChessModel.ROOK), args.rook])
        total_pieces += args.rook
    if args.knight:
        starting_pieces.append([ChessPiece(ChessModel.KNIGHT), args.knight])
        total_pieces += args.knight
    if args.bishop:
        starting_pieces.append([ChessPiece(ChessModel.BISHOP), args.bishop])
        total_pieces += args.bishop


    table = ChessTable(starting_pieces)
    table.x_size = args.x
    table.y_size = args.y
    table.prepare()

    good_config = True
    if len(starting_pieces) == 0:
        print "You need to add at least one type of chess piece"
        good_config = False

    if args.x * args.y < total_pieces:
        print "Not enough tiles for all pieces."
        good_config = False

    if not good_config:
        #configuration error
        parser.print_usage()
        sys.exit()

    #start solving
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
