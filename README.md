# PuzzleADaySolver
Command line tool to solve the [DragonFjord Puzzle-A-Day](https://www.dragonfjord.com/product/a-puzzle-a-day/) puzzle for any day/month.

Based on https://github.com/aydinschwa/Puzzle-Solver

```
$ python PuzzleADaySolver.py
Usage: PuzzleADaySolver <month> <day>
Month must be between 1 and 12 and day must be between 1 and 31

$ python PuzzleADaySolver.py 5 1
Solutions: 1
Iterations: 77

1 1 1 4 X 4
1 1 1 4 4 4
X 2 8 3 3 3 3
7 2 8 8 8 5 3
7 2 2 2 8 5 5
7 7 6 6 6 5 5
7 6 6

Solutions: 2
Iterations: 728

1 1 1 4 X 4
1 1 1 4 4 4
X 7 7 7 7 3 3
8 8 7 6 6 6 3
2 8 6 6 5 5 3
2 8 8 5 5 5 3
2 2 2

...

Solutions: 57
Iterations: 27,493

5 5 7 4 X 4
5 5 7 4 4 4
X 5 7 7 6 8 8
3 3 7 6 6 8 2
3 1 1 6 8 8 2
3 1 1 6 2 2 2
3 1 1


There are 57 solutions.
