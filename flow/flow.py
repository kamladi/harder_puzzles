from random import randint

# Pipe object to connect End Points
class Pipe(object):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "Pipe:" + str(self.color)

# End Points set at beginning of game
class EndPoint(object):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "End:" + str(self.color)

# solve a flow board
class FlowSolver(object):

    def solve(self, board):
        return

# Flow board and moves
class FlowPuzzle(object):
    def __init__(self, size, starting_board):
        self.size = size
        # map of starting boards (from last level of game)
        self.starting_board = starting_board
        self.board = self.make_init_board()

    # create an initial board based on size
    def make_init_board(self):
        board = [[None for _ in xrange(self.size)] for _ in xrange(self.size)]
        # randomly place end points
        for color in self.starting_board:
            for (r,c) in self.starting_board[color]:
                board[r][c] = EndPoint(color)
        return board

    # see if a move is valid
    def is_valid_move(self, color, row, col):
        return self.is_in_bounds(row,col) and self.board[row][col] is None
        
    # apply a move to the board
    def apply_move(self, color, row, col):
        self.board[row][col] = Pipe(color)

    # undo a move at a particular row and column
    def undo_move(self, row, col):
        self.board[row][col] = None

    # get all valid moves
    def get_valid_moves(self, color, row, col):
        possibilities = [(1,0), (-1,0), (0,1), (0,-1)]

        moves = []
        for r, c in possibilities:
            if self.is_valid_move(color, row + r, col + c):
                moves.append((color, row + r, col + c))
                
        return moves

    # get a random move by moving a starting or ending point
    def get_random_move(self):
        # get a random move for a random color
        color = randint(0,len(self.starting_board)-1)
        start, end = self.starting_board[color]
        while self.is_solved_color(color, start[0], start[1], end):
            color = (color + 1) % self.size
            start, end = self.starting_board[color]

        start_end = randint(0,1)
        row, col = self.starting_board[color][start_end]
        moves = self.get_valid_moves(color, row, col)
        print moves
        selected = randint(0,len(moves)-1)
        return moves[selected]

    # check if board is solved
    def is_solved(self):
        # check that entire grid is not None
        for r in xrange(self.size):
            for c in xrange(self.size):
                if self.board[r][c] is None:
                    return False
        # check that all end points are connected
        for color in self.starting_board:
            start, end = self.starting_board[color]
            if not self.is_solved_color(color, start[0], start[1], end):
                return False
        return True

    # check if a particular color is already solved using flood fill
    def is_solved_color(self, color, row, col, end):
        if (row, col) == end:
            return True
        if not self.is_in_bounds(row, col):
            return False
        if self.board[row][col] is None:
            return False
        if self.board[row][col].color != color:
            return False
        return (self.is_solved_color(color, row+1, col, end) or
            self.is_solved_color(color, row-1, col, end) or
            self.is_solved_color(color, row, col+1, end) or
            self.is_solved_color(color, row, col-1, end))

    # see if coordinates are in bounds on the board
    def is_in_bounds(self, r, c):
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            return False
        return True

    # print out a game board
    def print_board(self):
        for row in self.board:
            for col in row:
                print str(col).ljust(7),
            print

# generate a puzzle
class FlowGenerator(object):

    def generate_puzzles(self, puzzle, solver, branching_factor, step, iterations):
        return

starting_pos = {
    2: {0: [(0,0),(1,0)], 1: [(0,1),(1,1)]},
    5: {0: [(0,0),(3,2)], 1: [(0,4),(4,2)], 2: [(2,1),(4,1)], 3: [(4,0),(2,2)]},
    6: {0: [(1,0),(3,5)], 1: [(1,1),(4,5)], 2: [(1,3),(4,4)], 3: [(2,1),(4,1)], 4: [(5,0),(3,1)]},
    7: {},
    8: {},
    9: {}
}

n = 5
P = FlowPuzzle(n, starting_pos[n])
P.apply_move(2, 3, 1)
P.print_board()
(color, r, c) = P.get_random_move()
P.apply_move(color, r, c)
P.print_board()
S = FlowSolver()
G = FlowGenerator()
