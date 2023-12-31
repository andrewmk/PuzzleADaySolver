import sys

class PuzzleADaySolver:

    def __init__(self, month, day, just_count = False):

        self.just_count = just_count

        self.pieces = (

            [],

            [[1, 1, 1],
             [1, 1, 1]],

            [[2, 0, 0],
             [2, 0, 0],
             [2, 2, 2]],

            [[3, 0],
             [3, 0],
             [3, 0],
             [3, 3]],

            [[4, 4, 4],
             [4, 0, 4]],

            [[5, 0],
             [5, 5],
             [5, 5]],

            [[6, 0],
             [6, 6],
             [0, 6],
             [0, 6]],

            [[7, 0],
             [7, 7],
             [7, 0],
             [7, 0]],

            [[8, 8, 0],
             [0, 8, 0],
             [0, 8, 8]]
        )

        self.board = [[0, 0, 0, 0, 0, 0, 0].copy() for _ in range(7)]
        self.board[0][6] = ' '
        self.board[1][6] = ' '
        self.board[6][3] = ' '
        self.board[6][4] = ' '
        self.board[6][5] = ' '
        self.board[6][6] = ' '
        
        month = month -1
        month_row = 0
        if month > 5:
            month_row = 1
            month = month - 6
        
        self.board[month_row][month] = 'X';
        
        day = day - 1
        day_row = 2 + (day // 7)
        day_col = day % 7
        
        self.board[day_row][day_col] = 'X';
        
        self.piece_positions = self.gen_piece_positions(self.pieces)

        self.iterations = 0
        self.solutions = []
        self.terminate = False

    def draw_board(self, board):
        for row in board:
            out_row = []
            for cell in row:
                out_row.append(str(cell))
            print(" ".join(out_row))
        print()

    @staticmethod
    def rotate_piece(piece):
        return [list(row[::-1]) for row in zip(*piece)]

    def get_rotations(self, piece):
        unique_rotations = [piece]
        for _ in range(3):
            piece = self.rotate_piece(piece)
            if piece not in unique_rotations:
                unique_rotations.append(piece)

        return unique_rotations, len(unique_rotations)

    @staticmethod
    def reflect_piece_x(piece):
        return piece[::-1]

    @staticmethod
    def reflect_piece_y(piece):
        return [row[::-1] for row in piece]

    def get_all_positions(self, piece):
        positions, _ = self.get_rotations(piece)
        for pos in positions:
            y_reflect = self.reflect_piece_y(pos)
            x_reflect = self.reflect_piece_x(pos)
            if y_reflect not in positions:
                positions.append(y_reflect)
            if x_reflect not in positions:
                positions.append(x_reflect)
        return positions

    def gen_piece_positions(self, pieces):
        piece_positions = []
        for piece in pieces[1:]:
            piece_positions.append(self.get_all_positions(piece))
        return piece_positions

    @staticmethod
    def legal_islands(board):
        # use bfs to find number of distinct islands
        board = [[elem for elem in row] for row in board]
        board_height = len(board)
        board_width = len(board[0])
        island_cells = []

        def island_bfs(row, col):
            cell_queue = [(row, col)]

            while cell_queue:
                row, col = cell_queue.pop()
                if board[row][col] != 0:
                    continue
                island_cells.append((row, col))
                board[row][col] = "#"
                for row_offset, col_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    temp_row = row + row_offset
                    temp_col = col + col_offset
                    if 0 <= temp_row < board_height and 0 <= temp_col < board_width and board[temp_row][temp_col] == 0:
                        cell_queue.append((temp_row, temp_col))

        for row in range(board_height):
            for col in range(board_width):
                if board[row][col] == 0:
                    island_bfs(row, col)
                    island_size = len(island_cells)

                    if island_size % 5 != 0:
                        return False

                    island_cells = []
        return True

    def add_piece(self, board, piece, start_row, start_col, check_islands=True):
        piece_width = len(piece[0])
        piece_height = len(piece)
        legal_move = True
        if (start_row + piece_height > len(board)) or (start_col + piece_width > len(board[0])):
            legal_move = False
            return board, legal_move

        changed_squares = []
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                # only add filled spaces, never take away
                if val:
                    # don't overwrite existing pieces on the board
                    if board[start_row + i][start_col + j]:
                        legal_move = False
                        return board, legal_move
                    else:
                        changed_squares.append((start_row + i, start_col + j, val))

        new_board = [[val for val in row] for row in board]
        for changed_row, changed_col, val in changed_squares:
            new_board[changed_row][changed_col] = val

        # check if the move created any illegal islands
        if check_islands and (not self.legal_islands(new_board)):
            legal_move = False
            return board, legal_move

        return new_board, legal_move

    def get_legal_squares(self, board, piece, check_islands=True):
        legal_moves = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                _, legal_move = self.add_piece(board, piece, row, col, check_islands)
                if legal_move:
                    legal_moves.append((row, col))
        return legal_moves

    def solve_board(self, board, pieces):

        self.iterations += 1

        if self.terminate:
            return

        # win condition is whole board is covered in pieces
        if all([all(row) for row in board]):
            self.solutions.append(board)
            if not self.just_count:
                print(f"Solution #{len(self.solutions):,}")
                print(f"Iterations: {self.iterations:,}\n")
                self.draw_board(board)
            return board
        else:
            piece_positions = pieces[0]
          
            for position in piece_positions:
                legal_squares = self.get_legal_squares(board, position)
                for row, col in legal_squares:
                    self.solve_board(self.add_piece(board, position, row, col)[0], pieces[1:])

    def run(self):
        self.solve_board(self.board, self.piece_positions)
        print(f"\n\nThere are {len(self.solutions)} solutions.")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        month = int(sys.argv[1])
        day = int(sys.argv[2])
        just_count = False
        if len(sys.argv) > 3:
          if sys.argv[3] == "--count":
            just_count = True
        if (month >= 1) and (month <= 12) and (day >= 1) and (day <= 31):
            PuzzleADaySolver(month, day, just_count).run()
        else:
            print("Usage: PuzzleADaySolver <month> <day> [--count]\nMonth must be between 1 and 12 and day must be between 1 and 31")
    else:
        print("Usage: PuzzleADaySolver <month> <day> [--count]\nMonth must be between 1 and 12 and day must be between 1 and 31")
