# Chess Solver

## Problem
The problem is to find all unique configurations of a set of normal chess pieces on a chess board with dimensions M×N where none of the pieces is in a position to take any of the others. Assume the colour of the piece does not matter, and that there are no pawns among the pieces.
Write a program which takes as input:
The dimensions of the board: M, N
The number of pieces of each type (King, Queen, Bishop, Rook and Knight) to try and place on the board.
As output, the program should list all the unique configurations to the console for which all of the pieces can be placed on the board without threatening each other.
When returning your solution, please provide with your answer the total number of unique configurations for a 7×7 board with 2 Kings, 2 Queens, 2 Bishops and 1 Knight. Also provide the time it took.

## Install
To start , in terminal run;
```
python chessSolver.py 7 7 --king=2 --queen=2 --bishop=2 --knight=1
```

## Example solutions
### 4x4 Table with 2 Rooks and 4 Knights
```
$ python chessSolver.py
Latest 3 tables:
|.|.|R|.
|.|N|.|N
|R|.|.|.
|.|N|.|N

|.|.|.|R
|N|.|N|.
|.|R|.|.
|N|.|N|.

|R|.|.|.
|.|N|.|N
|.|.|R|.
|.|N|.|N

Total possibilities:
8
Time in seconds:
0.0197401046753
```
### 7x7 Table with 2 Kings, 2 Queens, 2 Bishops and 1 Knight
```
Latest 3 tables:
|K|.|K|.|.|.|B
|.|.|.|.|Q|.|.
|.|Q|.|.|.|.|.
|.|.|.|.|.|.|.
|B|.|.|.|.|N|.
|.|.|.|.|.|.|.
|.|.|.|.|.|.|.

|K|.|K|.|.|.|.
|.|.|.|.|Q|.|.
|.|Q|.|.|.|.|.
|.|.|.|.|.|.|.
|B|.|B|.|.|N|.
|.|.|.|.|.|.|.
|.|.|.|.|.|.|.

|K|.|K|.|.|.|B
|.|.|.|.|Q|.|.
|.|Q|.|.|.|.|.
|.|.|.|.|.|.|.
|.|.|.|.|.|N|.
|.|.|B|.|.|.|.
|.|.|.|.|.|.|.

Total possibilities:
3063828
Time in seconds:
1921.78499985
```
