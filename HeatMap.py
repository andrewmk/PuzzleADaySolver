import PuzzleADaySolver as p

for month in range(1, 13):
    for day in range(1, 32):
        solver = p.PuzzleADaySolver(month, day, True)
        solver.solve_board(solver.board, solver.piece_positions)
        num_solutions = len(solver.solutions)
        print(f"{num_solutions}, ", end = '', flush = True)
    print("")
